#!/usr/bin/env python3
"""Run syntax checks and unittest discovery for the repository."""

from __future__ import annotations

from pathlib import Path
import py_compile
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = ROOT / "src"
TESTS_ROOT = ROOT / "tests"
PACKAGE_ROOT = SRC_ROOT / "ucb_to_testflight"


def _compile_sources() -> None:
    assert PACKAGE_ROOT.exists(), f"Missing package root: {PACKAGE_ROOT}"
    assert (PACKAGE_ROOT / "__init__.py").exists(), "Missing __init__.py"

    for source_file in sorted(PACKAGE_ROOT.glob("*.py")):
        py_compile.compile(str(source_file), doraise=True)

    for test_file in sorted(TESTS_ROOT.rglob("test_*.py")):
        py_compile.compile(str(test_file), doraise=True)


def _run_tests() -> None:
    sys.path.insert(0, str(SRC_ROOT))
    suite = unittest.defaultTestLoader.discover(
        start_dir=str(TESTS_ROOT),
        pattern="test_*.py",
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)


def main() -> None:
    _compile_sources()
    _run_tests()
    print("tests/run_all.py: PASS")


if __name__ == "__main__":
    main()
