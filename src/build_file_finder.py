"""
Looks for the build file in the environment variable OUTPUT_DIRECTORY.

Made for Unity Cloud Build .ipa and .aab files.
Executable path is OUTPUT_DIRECTORY/executable_name.type for UCB.
PS. UCB does expose the full path but it's in an API that I can't be bothered touching (https://build-api.cloud.unity3d.com/docs).
"""
import os
from pathlib import Path
from typing import Iterator

class BuildFileFinder:
    file_extension: str
    file_path: Path
    _output_directory: Path

    def __init__(self, output_directory: Path, file_extension: str):
        self._output_directory = output_directory
        self._set_file_extension(file_extension)
        self._find_and_set_file()

    def _set_file_extension(self, file_extension: str) -> None:
        """ Set self.file_extension as a lowercase version of file_extension and add "." prefix if required. """
        self.file_extension = file_extension.lower()
        if not self.file_extension.startswith("."):
            self.file_extension = "." + file_extension

    def _find_and_set_file(self) -> None:
        self.file_path = self._find_file()
        if self.file_path is None:
            raise FileNotFoundError(f"No {self.file_extension} found.")

    def _find_file(self) -> Path:
        for searcher in [self._search_output_directory]:    # If you want to search more places, add functions to this list
            path = searcher()
            if path: 
                return path

        raise FileNotFoundError(f"No {self.file_extension} file found!")

    def _search_output_directory(self):
        """
        Get file at $OUTPUT_DIRECTORY/build_name.type
        If $OUTPUT_DIRECTORY doesn't exist or the file doesn't, return None
        """
        if not self._output_directory.exists():
            text = f"$OUTPUT_DIRECTORY ({self._output_directory.resolve()}) doesn't exist!"
            raise FileNotFoundError(text)
        return self._choose_file(list(self._search_path(self._output_directory)))

    def _search_path(self, root: Path, recursive=False) -> Iterator:
        for file_name in os.listdir(root):
            file_path = Path(os.path.join(root, file_name))

            if file_path.is_dir() and recursive:
                yield from self._search_path(file_path, recursive)

            if not file_path.is_file(): continue
            if not file_path.suffix.lower() == self.file_extension: continue

            yield file_path

    def _choose_file(self, paths: list):
        if len(paths) == 0:
            raise FileNotFoundError(f"Could not find any {self.file_extension} files in {str(self._output_directory.resolve())}")

        if len(paths) == 1:
            return paths[0]

        print(f"Found {len(paths)} {self.file_extension} files:")
        for file_path in paths:
            print(f"  - {file_path}")

        print("TODO: Write a smarter searcher. Taking first...")
        return paths[0]


def find_build_file_path(output_directory: Path, extension: str) -> Path:
    return BuildFileFinder(output_directory, extension).file_path