#!/usr/bin/env python3
"""OpenAI-backed country normalization.

This module provides a single public helper, :func:`suggest_country_fix`, which
uses the OpenAI Responses API to normalize a free-form country string to a
canonical country name + ISO-3166 alpha-3 code.

The core design goals are:

1) Constrained outputs
   The model must choose from an *explicit* allow-list of ISO-3 codes and
   canonical country names. The JSON Schema uses ``enum`` to hard constrain the
   model, and the schema is configured as strict.

2) Safe failure mode
   If the input is ambiguous or the model is not confident enough, the model is
   instructed to return ``best_* = null`` and ``needs_review = true`` rather
   than guessing. We also apply a defensive post-check locally.

3) Explainability
   The response schema includes ``reason`` fields and up to 5 ranked candidates
   to help users understand and audit the choice.

The OpenAI Python SDK has changed its structured output parameter naming across
versions. This code prefers the openai==2.x style:

    ``responses.create(..., text={"format": {"type": "json_schema", ...}})``

and falls back to the older ``response_format=...`` argument if needed.

Inputs
------
``user_text``
    Free-form user input (may be misspelled, have accents, abbreviations, etc.).
``allowed_iso3``
    List of canonical ISO-3166 alpha-3 codes the model is allowed to output.
``allowed_names``
    List of canonical country names the model is allowed to output.

Output
------
Returns a ``dict[str, Any]`` matching the strict JSON schema built by
:func:`_build_response_schema`.
"""

import json
import os
from typing import Any

from openai import OpenAI

from laser.init.utils import __name_mapping__

# ----------------------------
# Optional local pre-filtering
# ----------------------------


def _maybe_prefilter_candidates(
    user_text: str,
    allowed_iso3: list[str],
    allowed_names: list[str],
    top_k: int = 80,
) -> tuple[list[str], list[str]]:
    """Reduce candidate set to keep prompts smaller.

    Why this exists
    ---------------
    The OpenAI call includes the allow-list inside the user message.
    When ``allowed_names`` is large, this increases prompt tokens and latency.
    Prefiltering keeps the prompt smaller while still being deterministic.

    How it works
    ------------
    - If RapidFuzz is available, we rank candidate names by similarity to the
        input and keep the top ``top_k``.
    - Otherwise, we use a token containment heuristic.

    Args:
        user_text: The user's input string to match against.
        allowed_iso3: Full list of allowed ISO-3 codes.
        allowed_names: Full list of allowed country names.
        top_k: Maximum number of candidates to keep (default: 80).

    Returns:
        Tuple of (iso3_subset, names_subset) where:
        - iso3_subset: Filtered or full list of ISO-3 codes
        - names_subset: Top-k most similar country names to user_text
    """
    user_text_norm = (user_text or "").strip().lower()
    if not user_text_norm or top_k <= 0:
        return allowed_iso3, allowed_names

    # Try rapidfuzz if installed.
    try:
        from rapidfuzz import fuzz, process  # type: ignore

        # Rank names by similarity
        scored_names = process.extract(
            user_text_norm,
            allowed_names,
            scorer=fuzz.WRatio,
            limit=min(top_k, len(allowed_names)),
        )
        names_subset = [name for (name, score, _idx) in scored_names]

        # If the input looks like a code, keep all codes; else keep as-is.
        # (Codes list is usually small; if it's huge, you can also prefilter it.)
        iso3_subset = allowed_iso3
        return iso3_subset, names_subset

    except Exception:
        # Fallback: keep names containing any token, else keep first top_k
        tokens = [t for t in user_text_norm.replace(",", " ").split() if t]
        if not tokens:
            return allowed_iso3, allowed_names[:top_k]

        hits = []
        for name in allowed_names:
            ln = name.lower()
            if any(t in ln for t in tokens):
                hits.append(name)

        if hits:
            return allowed_iso3, hits[:top_k]
        return allowed_iso3, allowed_names[:top_k]


# ----------------------------
# Schema (Structured Outputs)
# ----------------------------


def _build_response_schema(allowed_iso3: list[str]) -> dict[str, Any]:
    """Build a JSON Schema for OpenAI structured outputs.

    Creates a strict JSON schema that constrains the model to return only allowed
    ISO-3 codes and provides structured country normalization results.

    Args:
        allowed_iso3: List of allowed ISO 3166-1 alpha-3 country codes.

    Returns:
        Dictionary containing a JSON schema configuration with:
        - type: "json_schema"
        - name: Schema identifier
        - schema: Complete JSON schema definition with enum constraints
        - strict: True (enforces strict adherence to schema)

    Why JSON Schema
    ---------------
    Structured outputs ensure the model returns machine-parseable JSON and
    prevents drifting into prose. A strict schema also makes error handling
    predictable.

    Why we hard constrain ISO-3 with ``enum``
    ----------------------------------------
    Putting the allowed ISO-3 codes into an ``enum`` makes it *impossible* for
    the model to return a different ISO-3 code (unless the SDK/model violates
    the contract). This is a key safety property.

    Tradeoff: schema size
    ---------------------
    If ``allowed_iso3`` is extremely large, the schema itself can become large.
    In that case you can remove the ``enum`` constraint and validate membership
    in application code instead.

    Why we set ``additionalProperties=false``
    ----------------------------------------
    This prevents the model from emitting unexpected keys that your downstream
    code might ignore silently.

    Why we require fields even when null
    -----------------------------------
    A response with stable keys is easier to log, validate, and join against.
    """
    return {
        "type": "json_schema",
        "name": "country_normalization",
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "input": {"type": "string"},
                "best_iso3": {"type": ["string", "null"], "enum": allowed_iso3 + [None]},
                "best_name": {"type": ["string", "null"]},
                "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                "needs_review": {"type": "boolean"},
                "reason": {"type": "string"},
                "candidates": {
                    "type": "array",
                    "maxItems": 5,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "iso3": {"type": ["string", "null"], "enum": allowed_iso3 + [None]},
                            "name": {"type": "string"},
                            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                            "reason": {"type": "string"},
                        },
                        "required": ["iso3", "name", "confidence", "reason"],
                    },
                },
            },
            "required": [
                "input",
                "best_iso3",
                "best_name",
                "confidence",
                "needs_review",
                "reason",
                "candidates",
            ],
        },
        "strict": True,
    }


# ----------------------------
# Main function
# ----------------------------


def suggest_country_fix(
    user_text: str,
    allowed_iso3: list[str],
    allowed_names: list[str],
    *,
    api_key: str,
    model: str = "gpt-5.2",
    prefilter_top_k: int | None = 80,
) -> dict[str, Any]:
    """
    Query OpenAI to normalize ``user_text`` to one of the allowed countries.

    Parameters
    ----------
    user_text:
        The raw user input to normalize.
    allowed_iso3 / allowed_names:
        The allow-lists used to constrain the model. These should be canonical
        (one spelling per country name).
    api_key:
        OpenAI API key. For CLI usage you typically read this from
        ``OPENAI_API_KEY`` and pass it in.
    model:
        The OpenAI model name to call.
    prefilter_top_k:
        If set, reduces the allowed country names to the top-k most similar
        before calling the model (to keep the prompt smaller).

    Returns
    -------
    A dict matching the JSON schema built by :func:`_build_response_schema`.

    Safety / quality behavior
    -------------------------
    - Constrained outputs: the schema and prompt instruct the model to select
      only from the allow-lists.
    - Conservative decision: if the model is not confident (or ambiguous), it
      returns ``best_* = null`` and ``needs_review = true``.
    - Explainability: includes reasons and up to 5 candidate suggestions.
    """
    if not allowed_iso3:
        raise ValueError("allowed_iso3 must be non-empty")
    if not allowed_names:
        raise ValueError("allowed_names must be non-empty")
    if not user_text or not user_text.strip():
        raise ValueError("user_text must be non-empty")

    # Optional prefilter to reduce token usage.
    # This is intentionally deterministic and purely a prompt-size optimization;
    # it should not change behavior when the candidate list is already small.
    if prefilter_top_k is not None:
        iso3_subset, names_subset = _maybe_prefilter_candidates(
            user_text=user_text,
            allowed_iso3=allowed_iso3,
            allowed_names=allowed_names,
            top_k=prefilter_top_k,
        )
    else:
        iso3_subset, names_subset = allowed_iso3, allowed_names

    # Build the structured output format.
    # In openai==2.x this is placed under `text={"format": ...}`.
    response_format = _build_response_schema(iso3_subset)

    system_instructions = (
        "You normalize messy user-provided country inputs to a canonical country.\n"
        "Hard rules:\n"
        "1) You may ONLY select from the provided allowed ISO-3 codes and allowed country names.\n"
        "2) If the input could match multiple countries (ambiguous) or confidence < 0.75, "
        "set best_iso3=null and best_name=null and needs_review=true.\n"
        "3) If confident, set best_iso3 to the ISO-3 code and best_name to the canonical "
        "full name.\n"
        "4) Provide up to 5 candidates ranked by likelihood.\n"
        "5) best_name must exactly match one of the provided allowed country names when not null.\n"
        "Return ONLY JSON matching the schema."
    )

    # Provide candidates to the model (names + codes).
    # This is the *actual* constraint surface: we want the model to see the full
    # allow-list (or a prefiltered subset) and not hallucinate.
    user_payload = {
        "user_input": user_text,
        "allowed_iso3": iso3_subset,
        "allowed_country_names": names_subset,
    }

    client = OpenAI(api_key=api_key)

    # OpenAI SDK call notes
    # ---------------------
    # `model=`: selects the model.
    # `input=`: the Responses API accepts either a plain string or a list of
    #           message objects. We pass an explicit system + user message to
    #           separate instructions from data.
    # `text={"format": ...}`: openai==2.x structured outputs. Passing a
    #           `{"type": "json_schema", ...}` object enforces JSON schema.
    #
    # Backward compatibility:
    # Some older SDK versions used `response_format=` instead of `text.format`.
    # We catch `TypeError` (unexpected kwarg) and retry with the old shape.
    try:
        resp = client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": system_instructions},
                # `ensure_ascii=False` keeps names like "Curaçao" readable.
                {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
            ],
            text={"format": response_format},
        )
    except TypeError:
        resp = client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
            ],
            response_format={"type": "json_schema", "json_schema": response_format},
        )

    # Parse the model output.
    # The OpenAI SDK exposes `output_text` as a convenience property containing
    # the concatenated text output. Under structured outputs this should be a
    # JSON object string.
    out = json.loads(resp.output_text)

    # Defensive post-validation (belt-and-suspenders)
    # ------------------------------------------------
    # Even though the schema + instructions should constrain outputs, we verify
    # `best_name` is a member of the allow-list. If it's not, we force manual
    # review rather than letting bad values propagate downstream.
    if out.get("best_name") is not None and out["best_name"] not in names_subset:
        out["best_iso3"] = None
        out["best_name"] = None
        out["needs_review"] = True
        out["confidence"] = min(float(out.get("confidence", 0)), 0.5)
        out["reason"] = "Model returned a best_name not in allowed list; forcing manual review."

    return out


# ----------------------------
# Example usage
# ----------------------------
if __name__ == "__main__":
    # Minimal demo (replace with your real lists)
    allowed_iso3 = list(set(__name_mapping__.values()))  # All ISO-3 codes in our mapping
    allowed_names = list(__name_mapping__.keys())  # All country names in our mapping

    # Demo usage expects an API key in the environment.
    # Never hardcode API keys into source files.
    API_KEY = os.environ.get("OPENAI_API_KEY")
    if not API_KEY:
        raise SystemExit(
            "Missing OPENAI_API_KEY. Set it in your environment to run this demo, e.g.\n"
            "  export OPENAI_API_KEY=..."
        )
    result = suggest_country_fix(
        "Madagaskar",
        allowed_iso3,
        allowed_names,
        api_key=API_KEY,
        # prefilter_top_k=50,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
