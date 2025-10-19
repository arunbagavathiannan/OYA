from pathlib import Path

# Set path values to centralize paths and simplify calls
BASE = Path(__file__).resolve().parents[1]
BACK_END = BASE / "back_end"
FRONT_END = BASE / "front_end"
DATA = BASE / "data"
UTILS = BASE / "utils"
NOTEBOOKS = BASE / "notebooks"

# data subfolder
STATE = DATA / "state"