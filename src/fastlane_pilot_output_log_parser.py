from typing import Iterator, Optional
from python_command_runner import OutputLine
from python_pretty_print import pretty_print


class Error:
    exception: Exception
    target_lines: list[OutputLine]
    hint: Optional[str]

    def __init__(self, exception: Exception, hint: Optional[str] = None, target_lines: list[OutputLine] = []) -> None:
        self.exception = exception
        self.target_lines = target_lines
        self.hint = hint

    def __str__(self) -> str:
        text = f"{type(self.exception).__name__}: {self.exception}"
        if self.hint is not None:
            text += f"\nHint: {self.hint}"
        return text


class ExceptionCollection(Exception):
    exceptions: list[Exception]

    def __init__(self, exceptions: list[Exception] = []) -> None:
        self.exceptions = exceptions
        super().__init__()

    @property
    def message(self) -> str:
        """Generate a summary message on the fly"""
        lines = [f"Exception collection of {len(self.exceptions)} exceptions"]
        for exception in self.exceptions:
            lines.append(f"{type(exception).__name__}({exception})")
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.message

    def __iter__(self):
        return iter(self.exceptions)


class CredentialsError(ValueError):
    pass


def success(log: list[str]) -> bool:
    # TODO
    return False


def raise_exceptions(lines: list[OutputLine]) -> None:
    errors: list[Error] = []
    for check in [_check_invalid_curve_name_error]:
        for error in check(lines):
            errors.append(error)

    if len(errors) == 0:
        return

    # all_log_lines = "\n".join(map(lambda line: line.text, lines))
    # pretty_print(f"<error>\n{'Full logs ':=<100}\n{all_log_lines}</error>")

    pretty_print(f"<error>\n{'Found errors in logs! ':=<100}</error>")
    for error in errors:
        print()
        _log_error(error)

    raise ExceptionCollection(list(map(lambda error: error.exception, errors)))


def _log_error(error: Error) -> None:
    pretty_print(f"<error>{error}</error>")
    for line in error.target_lines:
        pretty_print(f"<error> -> [{line.index}] {line.text}</error>")


def _check_invalid_curve_name_error(lines: list[OutputLine]) -> Iterator[Error]:
    for line in lines:
        if "[!] invalid curve name" in line.text.lower():
            error = Error(CredentialsError("API key check failed! (Found \"[!] invalid curve name\" in logs)"))
            error.target_lines = [line]
            error.hint = "Double check your api key values."
            yield error