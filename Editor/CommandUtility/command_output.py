class CommandOutput:
    stdout_lines: list = []
    return_code: int = -1

    def success(self) -> bool:
        return self.return_code == 0

