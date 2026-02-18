#!/usr/bin/env python3
"""Minimal package structure smoke checks."""

from pathlib import Path
import py_compile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "src" / "ucb_to_testflight"


def main() -> None:
    assert PACKAGE_ROOT.exists()
    assert (PACKAGE_ROOT / "__init__.py").exists()

    for source_file in PACKAGE_ROOT.glob("*.py"):
        py_compile.compile(str(source_file), doraise=True)

    print("tests/run_all.py: PASS")


if __name__ == "__main__":
    main()
