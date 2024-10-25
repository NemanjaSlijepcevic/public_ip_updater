import pytest  # noqa: F401
from file_utils import (
    write_current_value,
    read_previous_value,
    check_and_create_file
)


class TestReadWriteCurrentIp:

    # Successfully writes a valid IP address to a file
    def test_successful_ip_write(self):
        filename = 'current_ip.txt'
        ip = '192.168.1.1'
        write_current_value(ip)
        with open(filename, 'r') as file:
            content = file.read()
        assert content

    def test_write_exception(self, mocker):

        filename = 'current_ip.txt'
        ip = '192.168.1.1'

        mocker.patch('builtins.open', side_effect=OSError)
        mock_logger = mocker.patch('file_utils.logger')

        result = write_current_value(ip)
        assert result is None

        mock_logger.exception.assert_called_once_with(
            f"An unexpected error occurred while writing to file:"
            f" {filename}"
        )

    # Successfully reads and returns the content of an existing file
    def test_read_existing_file(self):
        expected_content = '192.168.1.1'
        result = read_previous_value()
        assert result == expected_content

    def test_read_non_existing(self, mocker):

        filename = 'current_ip.txt'
        mocker.patch('builtins.open', side_effect=FileNotFoundError)
        mock_logger = mocker.patch('file_utils.logger')

        result = read_previous_value()
        assert result is None

        mock_logger.error.assert_called_once_with(
            f"File not found: {filename}", exc_info=True
        )

    def test_read_exception(self, mocker):

        filename = 'current_ip.txt'

        mocker.patch('builtins.open', side_effect=IOError)
        mock_logger = mocker.patch('file_utils.logger')

        result = read_previous_value()
        assert result is None

        mock_logger.exception.assert_called_once_with(
            f"An unexpected error occurred while reading from file:"
            f" {filename}"
        )

    def test_check_file_not_exists(self, mocker):
        filename = 'current_ip.txt'
        mock_logger = mocker.patch('file_utils.logger')
        mocker.patch('os.path.exists', return_value=False)
        check_and_create_file()
        mock_logger.debug.assert_called_once_with(
            f"File '{filename}' has been created."
        )

    def test_check_file_exists(self, mocker):
        filename = 'current_ip.txt'
        mock_logger = mocker.patch('file_utils.logger')
        mocker.patch('os.path.exists', return_value=True)
        check_and_create_file()
        mock_logger.debug.assert_called_once_with(
            f"File '{filename}' already exists."
        )

    def test_check_file_not_exists_exception(self, mocker):
        filename = 'current_ip.txt'
        mock_logger = mocker.patch('file_utils.logger')
        mocker.patch('os.path.exists', return_value=False)
        mocker.patch('builtins.open', side_effect=OSError)
        check_and_create_file()
        mock_logger.exception.assert_called_once_with(
            f"An unexpected error occurred while creating a file:"
            f" {filename}"
        )
