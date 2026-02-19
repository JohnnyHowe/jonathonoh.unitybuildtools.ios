from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from ucb_to_testflight.build_file_finder import BuildFileFinder, find_build_file_path


class BuildFileFinderTests(unittest.TestCase):
    def test_finds_single_matching_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ipa_path = root / "game.ipa"
            ipa_path.write_text("binary", encoding="utf-8")

            finder = BuildFileFinder(root, ".ipa")

            self.assertEqual(finder.file_path, ipa_path)
            self.assertEqual(finder.file_extension, ".ipa")

    def test_normalizes_extension_without_dot_and_with_uppercase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ipa_path = root / "archive.IPA"
            ipa_path.write_text("binary", encoding="utf-8")

            finder = BuildFileFinder(root, "IPA")

            self.assertEqual(finder.file_extension, ".ipa")
            self.assertEqual(finder.file_path, ipa_path)

    def test_raises_when_output_directory_is_missing(self) -> None:
        missing_dir = Path(tempfile.gettempdir()) / "missing-does-not-exist-dir"

        with self.assertRaises(FileNotFoundError):
            BuildFileFinder(missing_dir, ".ipa")

    def test_raises_when_no_matching_files_are_found(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "game.txt").write_text("no build", encoding="utf-8")

            with self.assertRaises(FileNotFoundError):
                BuildFileFinder(root, ".ipa")

    def test_returns_first_file_when_multiple_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = root / "a.ipa"
            second = root / "b.ipa"
            first.write_text("1", encoding="utf-8")
            second.write_text("2", encoding="utf-8")

            found = find_build_file_path(root, ".ipa")

            self.assertIn(found, {first, second})


if __name__ == "__main__":
    unittest.main()
