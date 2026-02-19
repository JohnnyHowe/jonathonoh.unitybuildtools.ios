"""UCB adapter that delegates TestFlight upload execution to pyliot."""

import sys
from pathlib import Path
from importlib import import_module

from .build_file_finder import BuildFileFinder

# pyliot currently imports `overwrite_then_delete` as a top-level module name.
sys.modules.setdefault("overwrite_then_delete", import_module("python_command_line_helpers.overwrite_then_delete"))
from pyliot.upload_to_test_flight import upload_to_testflight as pyliot_upload_to_testflight


def upload_to_testflight(
	api_key_issuer_id: str,
	api_key_id: str,
	api_key_content: str,
	output_directory: Path,
	changelog: str,
	groups: list[str] = [],
	max_upload_attempts: int = 10,
	attempt_timeout_seconds: int = 600,
):
	ipa_path = BuildFileFinder(output_directory, ".ipa").file_path
	pyliot_upload_to_testflight(
		api_key_issuer_id=api_key_issuer_id,
		api_key_id=api_key_id,
		api_key_content=api_key_content,
		ipa_path=ipa_path,
		changelog=changelog,
		groups=groups,
		max_upload_attempts=max_upload_attempts,
		attempt_timeout_seconds=attempt_timeout_seconds,
	)
