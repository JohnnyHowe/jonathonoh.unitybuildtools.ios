from .command_utility import *
from .upload_configuration import UploadConfiguration
from CommandUtility.command import Command
from pretty_print import *


class TestflightUploader:
    verbose: bool
    last_altool_output = []
    configuration: UploadConfiguration
    command: Command

    _print_prefix: str = "[TestFlightUploader]"

    def __init__(self, configuration: UploadConfiguration) -> None:
        self.configuration = configuration
        self._create_command()

    def _create_command(self):
        self.command = Command()
        self.command.executable = "fastlane"
        self.command.subcommands = ["pilot", "upload"]
        self.command.add_flag_and_value("--ipa", str(self.configuration.ipa_path))
        self.command.add_flag_and_value("--api-key-path", str(self.configuration.app_store_key_path))
        self.command.add_flag_and_value("--changelog", f"\"{self._read_changelog()}\"")
        if self.configuration.test_groups:
            self.command.add_flag_and_value("--groups", self.configuration.test_groups)
        self.command.add_flag("--verbose")

    def upload(self):
        pretty_print(f"{self._print_prefix} running following command\n{self.command.to_str(newlines=True)}")

        for attempt_number in range(self.configuration.max_upload_attempts):

            pretty_print(f"Upload attempt {attempt_number + 1} of {self.configuration.max_upload_attempts}")
            command_output = self._try_upload_iteration()
            pretty_print(f"{self._print_prefix} have not yet written CommandOutput parser", color=ERROR)

        pretty_print(f"{self._print_prefix} Out of upload attempts!", color=ERROR)
        return 1
            
    def _try_upload_iteration(self) -> CommandOutput:
        pretty_print(f"{self._print_prefix} have not yet written _typ_upload_iteration", color=ERROR)
        return CommandOutput()

    def _read_changelog(self) -> str:
        with open(self.configuration.changelog_path, "r") as file:
            return file.read()