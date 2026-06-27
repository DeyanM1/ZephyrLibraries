from __future__ import annotations

# from base import ZCommand, ActiveVars, ZValue, Base    # <- for debugging. Use importHandler for final Project!


def importHandler(names: list[str]):
    import importlib.util
    from pathlib import Path
    import sys

    base_path = Path(__file__).resolve().parent / "base.py"

    moduleName = base_path.stem

    spec = importlib.util.spec_from_file_location(moduleName, base_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Failed to create spec for {base_path}")


    base = importlib.util.module_from_spec(spec)
    sys.modules[moduleName] = base
    spec.loader.exec_module(base)

    for name in names:
        globals()[name] = getattr(base, name)

importHandler(["Base", "ZCommand", "ActiveVars", "ZValue"])


class PYTHON(Base):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.supportedVars = []

        self.registerFunc({self.run: ""})

    def run(self, cmd: ZCommand, activeVars: ActiveVars):
        cmd.checkArgs(1)
        
        rawCommand = cmd.args[0]

        command = ZValue("", "PT")
        
        rawCommand.lstrip("(").rstrip(")")
        if rawCommand.startswith("'"):
            command.setValue(rawCommand, activeVars)
        else:
            command.value = rawCommand

        eval(command.value)



def load() -> dict[str, type]:
    return {"": PYTHON}
