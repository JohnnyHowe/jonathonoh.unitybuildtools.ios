import argparse
from pathlib import Path
from typing import Callable
from testflight_uploader.upload_configuration import UploadConfiguration
from testflight_uploader.testflight_uploader import TestflightUploader
from testflight_uploader.app_store_connect_key_creator import create_from_environment_variables as create_api_key_file


def main():
    verbose = True

    api_key_path = create_api_key_file()

    # Run the uploader safely
    def get_configuration_and_upload():
        configuration = UploadConfiguration(api_key_path, verbose)
        uploader = TestflightUploader(configuration, verbose)
        uploader.upload()
    error = _run_safe(get_configuration_and_upload)

    # Delete key if this script made it
    if is_api_key_auto_generated and api_key_path.exists():
        api_key_path.unlink()

    # Raise an error if there was one
    if error:
        raise error


def _run_safe(func: Callable):
    try:
        func()
        return None
    except Exception as exception:
        return exception


if __name__ == "__main__":
    main()