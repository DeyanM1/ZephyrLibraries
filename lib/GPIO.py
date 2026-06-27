from __future__ import annotations

import FakeRPi.GPIO as GPIO # type: ignore

# from base import ZError, ZCommand, ActiveVars, ZValue, Base    # <- for debugging. Use importHandler for final Project!


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

importHandler(["ZError", "ZCommand", "ActiveVars", "ZValue", "Base"])


class GPIO(Base):
    def __init__(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        super().__init__(cmd, activeVars)
        self.value = ZValue("~0", "BOOL") # Value of last read pin
        self.supportedVars = ["INT", "PT", "FLOAT", "BOOL"]



        self.firstTimeInit(cmd, activeVars)

        self.registerFunc({self.SETUP: "", self.SET: "", self.READ: "", self.CLEAN: "", self.w: ""})

        
    def firstTimeInit(self, cmd: ZCommand, activeVars: ActiveVars):
        self.w(cmd, activeVars)

    def onChange(self) -> str:
        return self.value.value
        
        
    # --- Callable Functions
     
    def w(self, cmd: ZCommand, activeVars: ActiveVars):
        cmd.checkArgs(1)
        
        boardType: ZValue = ZValue("", "PT")
        boardType.setValue(cmd.args[0], activeVars)
        
        match boardType.value:
            case "BCM":
                GPIO.setmode(GPIO.BCM) # type: ignore
            case "BOARD":
                GPIO.setmode(GPIO.BOARD) # type: ignore
            case _:
                print("ERROR: unknown board Type. SUPPORTED: BCM/BOARD")
                quit()

    def SETUP(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        cmd.checkArgs(2)
        
        pin: ZValue = ZValue("0",  "INT")
        pin.setValue(cmd.args[0], activeVars)
        
        pinType: ZValue = ZValue("", "PT")
        pinType.setValue(cmd.args[1], activeVars)

        match pinType.value:
            case "IN":
                GPIO.setup(int(pin.value), GPIO.IN) # type: ignore
            case "OUT":
                GPIO.setup(int(pin.value), GPIO.OUT) # type: ignore
            case _:
                raise ZError(114)
    
    
    def SET(self, cmd: ZCommand, activeVars: ActiveVars) -> None:
        cmd.checkArgs(2)
        
        pin: ZValue = ZValue("0", "INT")
        pin.setValue(cmd.args[0], activeVars)
        
        pinValue: ZValue = ZValue("~0", "BOOL")
        pinValue.setValue(cmd.args[1], activeVars)

        match pinValue.asPythonBOOL:
            case True:
                GPIO.output(int(pin.value), GPIO.HIGH) # type: ignore
            case False:
                GPIO.output(int(pin.value), GPIO.LOW) # type: ignore

    def READ(self, cmd: ZCommand, activeVars: ActiveVars):
        cmd.checkArgs(1)
        
        pin: ZValue = ZValue("0", "INT")
        pin.setValue(cmd.args[0], activeVars)


        rawValue = GPIO.input(int(pin.value))

        match rawValue:
            case 1:
                self.value.setValue("~1", activeVars)
            case 0:
                self.value.setValue("~0", activeVars)
            case _:
                pass

    def CLEAN(self, cmd: ZCommand, activeVars: ActiveVars):
        GPIO.cleanup() 


 

def load() -> dict[str, type]:
    return {"": GPIO}