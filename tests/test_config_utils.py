import os
import pytest
from config_utils import (
    check_bearer_token,
    check_api_url,
    check_frequency,
    check_file_data_path,
    check_log_level,
    check_inputs
)


class TestInputVariables:

    def test_check_bearer_token_empty(self, monkeypatch, mocker):
        monkeypatch.setenv("API_IP_TOKEN", "")
        mock_logger = mocker.patch('config_utils.logger')

        assert os.getenv("API_IP_TOKEN") == ""

        with pytest.raises(SystemExit) as e:
            check_bearer_token()
        assert e.type == SystemExit
        assert e.value.code == 1

        mock_logger.error.assert_called_once_with(
            "BEARER_TOKEN is not set."
        )

    def test_check_bearer_token_success(self, monkeypatch):
        monkeypatch.setenv("API_IP_TOKEN", "random_api_token")

        assert check_bearer_token()

    def test_check_api_url_empty(self, monkeypatch, mocker):
        monkeypatch.setenv("NODE_IP_DOMAIN", "")
        mock_logger = mocker.patch('config_utils.logger')

        assert os.getenv("NODE_IP_DOMAIN") == ""

        with pytest.raises(SystemExit) as e:
            check_api_url()
        assert e.type == SystemExit
        assert e.value.code == 1

        mock_logger.error.assert_called_once_with(
            "NODE_IP_DOMAIN is not set."
        )

    def test_check_api_url_success(self, monkeypatch):
        monkeypatch.setenv("NODE_IP_DOMAIN", "https://random-domain.com")

        assert check_api_url()

    def test_check_frequency_too_small(self, monkeypatch, mocker):
        monkeypatch.setenv("CHECK_FREQUENCY", "1")
        mock_logger = mocker.patch('config_utils.logger')

        assert os.getenv("CHECK_FREQUENCY") == "1"

        with pytest.raises(SystemExit) as e:
            check_frequency()
        assert e.type == SystemExit
        assert e.value.code == 1

        mock_logger.error.assert_called_once_with(
            "Incorrect value of frequency."
        )

    def test_check_frequency_incorrect(self, monkeypatch, mocker):
        monkeypatch.setenv("CHECK_FREQUENCY", "error")
        mock_logger = mocker.patch('config_utils.logger')

        assert os.getenv("CHECK_FREQUENCY") == "error"

        with pytest.raises(SystemExit) as e:
            check_frequency()
        assert e.type == SystemExit
        assert e.value.code == 1

        mock_logger.error.assert_called_once_with(
            "Incorrect value of frequency."
        )

    def test_check_frequency_success(self, monkeypatch):
        monkeypatch.setenv("CHECK_FREQUENCY", "50")

        assert check_frequency() == 50

    def test_check_FILE_DATA_PATH_error(self, monkeypatch, mocker):
        monkeypatch.setenv("FILE_DATA_PATH", "five")
        mock_logger = mocker.patch('config_utils.logger')

        assert os.getenv("FILE_DATA_PATH") == "five"

        with pytest.raises(SystemExit) as e:
            check_file_data_path()
        assert e.type == SystemExit
        assert e.value.code == 1

        mock_logger.error.assert_called_once_with(
            "Incorrect value of FILE_DATA_PATH."
        )

    def test_check_FILE_DATA_PATH_success(self, monkeypatch):
        monkeypatch.setenv("FILE_DATA_PATH", "random_api_token")

        assert check_file_data_path()

    def test_check_log_level_error(self, monkeypatch, mocker):
        monkeypatch.setenv("LOG_LEVEL", "not_working")
        mock_logger = mocker.patch('config_utils.logger')

        assert os.getenv("LOG_LEVEL") == "not_working"

        with pytest.raises(SystemExit) as e:
            check_log_level()
        assert e.type == SystemExit
        assert e.value.code == 1
        mock_logger.error.assert_called_once_with(
            "Invalid log level: 'NOT_WORKING'."
        )

    def test_check_log_level_success(self, monkeypatch):
        monkeypatch.setenv("LOG_LEVEL", "WARNING")

        assert check_log_level()

    def test_check_inputs_success(self, monkeypatch):
        monkeypatch.setenv("API_IP_TOKEN", "random_api_token")
        monkeypatch.setenv("NODE_IP_DOMAIN", "https://random-domain.com")
        monkeypatch.setenv("CHECK_FREQUENCY", "50")
        monkeypatch.setenv("FILE_DATA_PATH", "random_api_token")
        monkeypatch.setenv("LOG_LEVEL", "WARNING")

        assert check_inputs()

    def test_check_inputs_failed(self, monkeypatch, mocker):
        monkeypatch.setenv("API_IP_TOKEN", "random_api_token")
        monkeypatch.setenv("NODE_IP_DOMAIN", "https://random-domain.com")
        monkeypatch.setenv("CHECK_FREQUENCY", "five")
        monkeypatch.setenv("FILE_DATA_PATH", "random_api_token")
        monkeypatch.setenv("LOG_LEVEL", "WARNING")
        mock_logger = mocker.patch('config_utils.logger')

        with pytest.raises(SystemExit) as e:
            check_inputs()
        assert e.type == SystemExit
        assert e.value.code == 1

        mock_logger.error.assert_called_once_with(
            "Incorrect value of frequency."
        )
