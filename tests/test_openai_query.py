"""Tests for OpenAI-backed country normalization helper.

These tests ensure `suggest_country_fix` calls the OpenAI Responses API using the
SDK-supported structured output parameter (`text={"format": ...}`) and that the
post-validation logic correctly forces manual review when the model returns a
country name outside the allowed set.

If these tests fail, the most likely impact is that the project will either:
- crash at runtime due to an OpenAI SDK signature mismatch, or
- accept invalid country normalizations that are not constrained to the allowed list.
"""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


def _load_openai_query_module():
    project_root = Path(__file__).resolve().parents[1]
    module_path = project_root / "src" / "laser" / "init" / "openai_query.py"

    spec = importlib.util.spec_from_file_location("laser_init_openai_query", module_path)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestOpenAIQuery(unittest.TestCase):
    def test_suggest_country_fix_uses_text_format_json_schema(self):
        """Given allowed countries, when suggest_country_fix is called, then it uses `text.format`.

        Failure implies the code is still calling `responses.create(response_format=...)`,
        which crashes under openai==2.x with: unexpected keyword argument 'response_format'.
        """

        module = _load_openai_query_module()

        class FakeResponse:
            def __init__(self, output_text: str):
                self.output_text = output_text

        class FakeResponses:
            def __init__(self) -> None:
                self.last_kwargs = None

            def create(self, **kwargs):
                self.last_kwargs = kwargs
                return FakeResponse(
                    json.dumps(
                        {
                            "input": "Madagaskar",
                            "best_iso3": "MDG",
                            "best_name": "Madagascar",
                            "confidence": 0.9,
                            "needs_review": False,
                            "reason": "Common alternate spelling.",
                            "candidates": [
                                {
                                    "iso3": "MDG",
                                    "name": "Madagascar",
                                    "confidence": 0.9,
                                    "reason": "Close match.",
                                }
                            ],
                        }
                    )
                )

        class FakeClient:
            def __init__(self) -> None:
                self.responses = FakeResponses()

        class FakeOpenAI:
            def __init__(self, api_key: str):
                self._api_key = api_key
                self.responses = FakeClient().responses

        allowed_iso3 = ["USA", "MDG"]
        allowed_names = ["United States of America", "Madagascar"]

        client = FakeOpenAI("sk-test")
        module.OpenAI = lambda api_key: client

        out = module.suggest_country_fix(
            "Madagaskar",
            allowed_iso3,
            allowed_names,
            api_key="sk-test",
        )

        self.assertEqual(out["best_iso3"], "MDG")
        self.assertEqual(out["best_name"], "Madagascar")

        # Ensure we used the openai==2.x supported parameter shape.
        last_kwargs = client.responses.last_kwargs

        self.assertIn("text", last_kwargs)
        self.assertNotIn("response_format", last_kwargs)
        self.assertIn("format", last_kwargs["text"])
        self.assertEqual(last_kwargs["text"]["format"]["type"], "json_schema")
        self.assertTrue(last_kwargs["text"]["format"].get("strict"))

    def test_suggest_country_fix_forces_review_when_best_name_not_allowed(self):
        """Given a model output with disallowed best_name, when parsed, then needs_review is forced.

        Failure implies we might accept a normalization that doesn't match the canonical list,
        which can corrupt downstream joins keyed on canonical country names.
        """

        module = _load_openai_query_module()

        class FakeResponse:
            def __init__(self, output_text: str):
                self.output_text = output_text

        class FakeResponses:
            def create(self, **_kwargs):
                return FakeResponse(
                    json.dumps(
                        {
                            "input": "USA",
                            "best_iso3": "USA",
                            "best_name": "United States",  # not in allowed_names
                            "confidence": 0.99,
                            "needs_review": False,
                            "reason": "Looks right.",
                            "candidates": [
                                {
                                    "iso3": "USA",
                                    "name": "United States",
                                    "confidence": 0.99,
                                    "reason": "Looks right.",
                                }
                            ],
                        }
                    )
                )

        class FakeOpenAI:
            def __init__(self, api_key: str):
                self._api_key = api_key
                self.responses = FakeResponses()

        module.OpenAI = FakeOpenAI

        allowed_iso3 = ["USA"]
        allowed_names = ["United States of America"]

        out = module.suggest_country_fix(
            "USA",
            allowed_iso3,
            allowed_names,
            api_key="sk-test",
        )

        self.assertIsNone(out["best_iso3"])
        self.assertIsNone(out["best_name"])
        self.assertTrue(out["needs_review"])
        self.assertLessEqual(out["confidence"], 0.5)


if __name__ == "__main__":
    unittest.main()
