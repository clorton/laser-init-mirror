import shutil
from pathlib import Path

__yaml__ = """
data_dir: %%data_dir%%

datafiles:
    shape_data: %%shape_data%%
    cxr_data: %%cxr_data%%
    pop_data: %%pop_data%%
    exp_data: %%exp_data%%

simulation:
    nyears: 2
    r0: 2.5
    exposed_duration_shape: 4.5
    exposed_duration_scale: 1.0
    infectious_duration_mean: 7.0
    gravity_k: 500
    gravity_a: 1
    gravity_b: 1
    gravity_c: 2
    naive_population: true
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

        yaml = __yaml__.replace("%%data_dir%%", str(output_dir.absolute()))
        yaml = yaml.replace("%%shape_data%%", str(shape_filename.name))
        yaml = yaml.replace("%%cxr_data%%", str(cxr_filename.name))
        yaml = yaml.replace("%%pop_data%%", str(pop_filename.name))
        yaml = yaml.replace("%%exp_data%%", str(exp_filename.name))
        (Path(output_dir) / "config.yaml").write_text(yaml)

        source_dir = Path(__file__).parent.parent / "models"
        shutil.copy2(source_dir / f"{model.lower()}.py", Path(output_dir) / f"{model.lower()}.py")
        shutil.copy2(source_dir / "plot.py", Path(output_dir) / "plot.py")

        return
