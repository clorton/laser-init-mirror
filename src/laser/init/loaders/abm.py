from pathlib import Path

__yaml__ = """
datafiles:
    data-dir: %%data-dir%%
    shape-data: %%shape-data%%
    cxr-data: %%cxr-data%%
    pop-data: %%pop-data%%
    exp-data: %%exp-data%%

simulation:
    nyears: 10
    r0: 2.5
    exposed-duration-shape: 4.5
    exposed-duration-scale: 1.0
    infectious-duration-mean: 7.0

"""


class AbmLoader:
    def __init__(self) -> None:
        pass

    @staticmethod
    def description() -> str:
        return "Write an ABM model script loading data from the downloaded data sources."

    def emit_script(
        self,
        mode: str,
        model: str,
        shape_filename: Path,
        cxr_filename: Path,
        pop_filename: Path,
        exp_filename: Path,
        output_dir: Path,
    ) -> None:

        assert mode.upper() == "ABM", f"AbmLoader only supports ABM mode, got {mode}"

        yaml = __yaml__.replace("%%data-dir%%", str(output_dir))
        yaml = yaml.replace("%%shape-data%%", str(shape_filename.name))
        yaml = yaml.replace("%%cxr-data%%", str(cxr_filename.name))
        yaml = yaml.replace("%%pop-data%%", str(pop_filename.name))
        yaml = yaml.replace("%%exp-data%%", str(exp_filename.name))
        (Path(output_dir) / "config.yaml").write_text(yaml)

        return
