# path_setup.py
# Import this at the top of ANY test file to fix paths automatically

import sys
from pathlib import Path

def find_root(marker="pyproject.toml"):
    """Walk up from this file until we find the root marker"""
    current = Path(__file__).parent
    while current != current.parent:
        if (current / marker).exists():
            return current
        current = current.parent
    raise FileNotFoundError(f"Could not find root marker: {marker}")

ROOT = find_root()

# Add any folders you want accessible from any script
sys.path.append(str(ROOT / "backend"))
# Later you can add more:
# sys.path.append(str(ROOT / "models"))
# sys.path.append(str(ROOT / "utils"))