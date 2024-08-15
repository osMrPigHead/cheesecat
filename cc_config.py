__all__ = [
    "DEBUG"
]

from pathlib import Path

DEBUG = (Path(__file__).parent / ".debug").exists()
