import sys
from pathlib import Path

import matplotlib

# Draw off-screen, so tests run without a display (e.g. in CI).
matplotlib.use("Agg")

# The scripts live in arduino_radar/ and import each other by module name.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "arduino_radar"))
