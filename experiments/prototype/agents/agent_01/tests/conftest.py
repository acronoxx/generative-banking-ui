"""Makes the agent modules (ui, tools...) importable from the tests."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
