#!/usr/bin/env python3
"""Render only the contribution-city assets; preserve all other profile artwork."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import gen_assets  # noqa: E402


def main():
    print(gen_assets.contrib_static())
    print(gen_assets.contrib_animated())


if __name__ == "__main__":
    main()
