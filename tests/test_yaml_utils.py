import pytest  # noqa: F401
from yaml_utils import update_yaml_file, get_nested_value


class TestReadWriteYamlFile:

    def test_get_nested_value(self):
        data = {
            'http': {
                'middlewares': {
                    'default-whitelist': {
                        'ipAllowList': {
                            'sourceRange': ['1.2.3.4']
                        }
                    }
                }
            }
        }
        keys = [
            'http',
            'middlewares',
            'default-whitelist',
            'ipAllowList',
            'sourceRange'
        ]
        result = get_nested_value(data, keys)
        assert result == ['1.2.3.4']

    def test_get_nested_value_none(self):
        data = {
            'http': {
                'middlewares': {
                    'default-whitelist': {
                        'ipAllowList': {
                            'sourceRange': ['1.2.3.4']
                        }
                    }
                }
            }
        }
        keys = [
            'http',
            'middlewares',
            'nonexistent',
            'ipAllowList',
            'sourceRange'
        ]
        result = get_nested_value(data, keys)
        assert result is None

    # Successfully writes a valid IP address to a file
    def test_successful_ip_replace(self, mocker):
        filename = 'configuration.yml'
        previous = '192.168.0.1'
        current = '192.168.1.1'
        mock_logger = mocker.patch('yaml_utils.logger')

        update_yaml_file(previous, current)
        with open(filename, 'r') as file:
            file.read()

        mock_logger.info.assert_called_once_with(
            f"Replaced old IP address {previous} with new IP address"
            f" {current}"
        )
        update_yaml_file(current, previous)  # for repeating the test

    def test_successful_ip_write(self, mocker):
        filename = 'configuration.yml'
        previous = ''
        current = '192.168.3.1'
        mock_logger = mocker.patch('yaml_utils.logger')

        update_yaml_file(previous, current)
        with open(filename, 'r') as file:
            file.read()

        mock_logger.info.assert_called_once_with(
            f"Added new IP address: {current}"
        )

        # for repeating the test remove appended line
        with open(filename, 'r') as file:
            lines = file.readlines()

        with open(filename, 'w') as file:
            for line in lines:
                if '192.168.3.1' not in line.strip():
                    file.write(line)

    def test_empty_value(self, mocker):
        filename = 'configuration.yml'
        previous = '192.168.0.1'
        current = '192.168.1.1'
        FILE_DATA_PATH = (
            'http.middlewares.default-whitelist.ipAllowList.sourceRange'
        )
        mock_logger = mocker.patch('yaml_utils.logger')

        # take data and make a shitty file
        with open(filename, 'r') as file:
            lines = file.readlines()

        with open(filename, 'w') as file:
            for line in lines:
                if 'default-whitelist' not in line.strip():
                    file.write(line)

        update_yaml_file(previous, current)
        with open(filename, 'r') as file:
            file.read()

        mock_logger.error.assert_called_once_with(
            f"sourceRange not found in the YAML file at path: "
            f"{FILE_DATA_PATH}"
        )

        # fix the file
        with open(filename, 'w') as file:
            for line in lines:
                file.write(line)

    def test_read_exception(self, mocker):

        filename = 'configuration.yml'
        previous = '192.168.0.1'
        current = '192.168.1.1'

        mocker.patch('builtins.open', side_effect=FileNotFoundError)
        mock_logger = mocker.patch('yaml_utils.logger')

        result = update_yaml_file(previous, current)
        assert result is None

        mock_logger.error.assert_called_once_with(
            f"YAML file not found: {filename}", exc_info=True
        )

    def test_write_exception(self, mocker):

        filename = 'configuration.yml'
        previous = '192.168.0.1'
        current = '192.168.1.1'

        mocker.patch('builtins.open', side_effect=IOError)
        mock_logger = mocker.patch('yaml_utils.logger')

        result = update_yaml_file(previous, current)
        assert result is None

        mock_logger.exception.assert_called_once_with(
            f"An unexpected error occurred while updating YAML file: "
            f"{filename}"
        )
