from __future__ import annotations

import unittest
from unittest.mock import Mock, patch

from ucb_to_testflight.upload_to_testflight_cmd_entry import upload_to_testflight_cmd_entry


class UploadCmdEntryTests(unittest.TestCase):
    def test_entry_loads_parameters_and_calls_uploader(self) -> None:
        with (
            patch("ucb_to_testflight.upload_to_testflight_cmd_entry.UploadParameters") as params_cls,
            patch("ucb_to_testflight.upload_to_testflight_cmd_entry.upload_to_testflight") as upload_func,
        ):
            params_instance = params_cls.return_value
            params_instance.load = Mock()
            params_instance.get_values = Mock(return_value=["a", "b", "c"])

            upload_to_testflight_cmd_entry()

            params_instance.load.assert_called_once_with()
            params_instance.get_values.assert_called_once_with()
            upload_func.assert_called_once_with("a", "b", "c")


if __name__ == "__main__":
    unittest.main()
