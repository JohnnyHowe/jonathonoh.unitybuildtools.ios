import sys
from pathlib import Path

# TODO find better solution to this
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pretty_print import *


class Command:
    executable: str = ""
    subcommands: list = []
    positional_args: list = []
    flags: list = []

    def add_flag_and_value(self, flag: str, value: str) -> None:
        """ Flag should include "-" prefix. """
        if not flag.startswith("-"):
            pretty_print(f"[CommandUtility] Flag added without \"-\" prefix ({flag}). Did you mean to do this?")
        self.flags.append(f"{flag} {value}")

    def add_flag(self, flag: str) -> None:
        """ Flag should include "-" prefix. """
        if not flag.startswith("-"):
            pretty_print(f"[CommandUtility] Flag added without \"-\" prefix ({flag}). Did you mean to do this?")
        self.flags.append(flag)

    def get_as_list(self) -> list:
        return [self.executable] + self.subcommands + self.positional_args + self.flags

    def __str__(self) -> str:
        sub_commands_str = " ".join(self.subcommands)
        flags_str = " ".join(self.flags)
        positional_args_str = " ".join(self.positional_args)

        result = ""
        for part in [self.executable, sub_commands_str, positional_args_str, flags_str]:
            if len(part.strip()) > 0:
                result += part + " "
        return result.strip()
        
    def to_str(self, newlines: bool = False) -> str:
        sub_commands_str = " ".join(self.subcommands)
        result = f"{self.executable} {sub_commands_str}"

        for part in self.positional_args + self.flags:
            if newlines:
                result += " \\ \n  "
            result += part

        return result.strip()