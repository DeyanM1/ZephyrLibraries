from __future__ import annotations

import math

# from base import ZCommand, ActiveVars, Base, ZError    # <- for debugging. Use importHandler for final Project!


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

importHandler(["ZCommand", "ActiveVars", "Base", "ZError"])


class MATH(Base):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
    

        self.registerFunc({self.fact: "", self.abs: "", self.setPI: "", self.sqrt: ""})

    def fact(self, cmd: ZCommand, activeVars: ActiveVars):
        cmd.checkArgs(1)
        
        var1 = activeVars.get(cmd.args[0])
        if not var1:
            raise ZError(113)

        var1.value.setValue(str(math.factorial(int(var1.value.value))), activeVars) 

        activeVars.update({var1.name: var1}) 
        return activeVars

    def abs(self, cmd: ZCommand, activeVars: ActiveVars):      
        cmd.checkArgs(1)
        
        var1 = activeVars.get(cmd.args[0])
        if not var1:
            raise ZError(113)
                    
        var1.value.setValue(str(abs(float(var1.value.value))), activeVars)  

        activeVars.update({var1.name: var1}) 
        return activeVars

    def setPI(self, cmd: ZCommand, activeVars: ActiveVars):       
        cmd.checkArgs(1)
        
        var1 = activeVars.get(cmd.args[0])
        if not var1:
            raise ZError(113)

        var1.value.setValue(str(math.pi), activeVars)  

        activeVars.update({var1.name: var1}) 
        return activeVars

    def sqrt(self, cmd: ZCommand, activeVars: ActiveVars):
        cmd.checkArgs(1)
        
        var1 = activeVars.get(cmd.args[0])
        if not var1:
            raise ZError(113)
            
        var1.value.setValue(str(math.sqrt(float(var1.value.value))), activeVars)  

        activeVars.update({var1.name: var1}) 
        return activeVars

 

def load() -> dict[str, type]:
    return {"": MATH}
