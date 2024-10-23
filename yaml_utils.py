import os
import yaml
import logging


FILE_DATA_PATH = os.getenv(
    'FILE_DATA_PATH',
    'http.middlewares.default-whitelist.ipAllowList.sourceRange'
)
TARGET_FILE = 'configuartion.yml'
logger = logging.getLogger(__name__)


# Function to access nested dictionary keys dynamically
def get_nested_value(data, keys):
    for key in keys:
        data = data.get(key)
        if data is None:
            return None
    return data


# Function to update the sourceRange list in the YAML file
def update_yaml_file(previous_value, current_value):
    try:
        logger.debug(f"Reading from YAML file: {TARGET_FILE}")
        with open(TARGET_FILE, 'r') as file:
            data = yaml.safe_load(file)

        # Split the source range path from variable into a list of keys
        source_range_keys = FILE_DATA_PATH.split('.')
        source_range = get_nested_value(data, source_range_keys)

        if source_range is None:
            logger.error(
                f"sourceRange not found in the YAML file at path: "
                f"{FILE_DATA_PATH}"
            )
            return

        if previous_value in source_range:
            index = source_range.index(previous_value)
            source_range[index] = current_value
            logger.info(
                f"Replaced old IP address {previous_value} with new IP address"
                f" {current_value}"
            )
        elif current_value not in source_range:
            source_range.append(current_value)
            logger.info(f"Added new IP address: {current_value}")

        logger.debug(f"Writing updated data to YAML file: {TARGET_FILE}")
        with open(TARGET_FILE, 'w') as file:
            yaml.dump(data, file)
    except FileNotFoundError:
        logger.error(f"YAML file not found: {TARGET_FILE}", exc_info=True)
    except Exception:
        logger.exception(
            f"An unexpected error occurred while updating YAML file: "
            f"{TARGET_FILE}"
        )
