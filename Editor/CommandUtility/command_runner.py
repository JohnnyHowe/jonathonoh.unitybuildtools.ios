from CommandUtility.command import Command


class CommandRunner:
    def __init__(self, command: Command) -> None:
        self.command = command
