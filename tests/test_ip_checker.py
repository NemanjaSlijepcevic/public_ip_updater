from ip_checker import get_current_value
import requests
import pytest  # noqa: F401


class TestGetCheckIp:

    # Successfully retrieves the public IP address from the external service
    def test_successful_ip_retrieval(self, mocker):
        mock_response = mocker.Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'ip': '192.168.1.1'}
        mocker.patch('requests.get', return_value=mock_response)

        ip = get_current_value()

        assert ip == '192.168.1.1'

    def test_empty_ip_retrieval(self, mocker):
        mock_response = mocker.Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'ip': ''}
        mocker.patch('requests.get', return_value=mock_response)
        mock_logger = mocker.patch('ip_checker.logger')

        get_current_value()

        mock_logger.error.assert_called_once_with(
            "IP address not found in the API response."
        )

    # Handles HTTP errors gracefully and logs the error
    def test_http_error_handling(self, mocker):
        mock_response = mocker.Mock()
        mock_response.raise_for_status.side_effect = (
            requests.exceptions.HTTPError("404 Client Error")
        )
        mocker.patch('requests.get', return_value=mock_response)
        mock_logger = mocker.patch('ip_checker.logger')

        ip = get_current_value()

        assert ip is None
        mock_logger.error.assert_called_once_with(
            "HTTP error occurred: 404 Client Error", exc_info=True
        )

    def test_http_get_exception(self, mocker):
        mock_response = mocker.Mock()
        mock_response.raise_for_status.side_effect = (
            requests.exceptions.ConnectionError("508 Error")
        )
        mocker.patch('requests.get', return_value=mock_response)
        mock_logger = mocker.patch('ip_checker.logger')

        ip = get_current_value()

        assert ip is None
        mock_logger.exception.assert_called_once_with(
            "An unexpected error occurred during GET request."
        )
