import logging


logger = logging.getLogger(__name__)
PREVIOUS_VALUE_FILE = 'current_ip.txt'


# Function to read the previous value from a file
def read_previous_value():
    try:
        logger.debug(f"Reading from file: {PREVIOUS_VALUE_FILE}")
        with open(PREVIOUS_VALUE_FILE, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        logger.error(
            f"File not found: {PREVIOUS_VALUE_FILE}", exc_info=True
        )
        return None
    except Exception:
        logger.exception(
            f"An unexpected error occurred while reading from file:"
            f" {PREVIOUS_VALUE_FILE}"
        )
        return None


# Function to write the current value to a file
def write_current_value(value):
    try:
        logger.debug(f"Writing to file: {PREVIOUS_VALUE_FILE}")
        with open(PREVIOUS_VALUE_FILE, 'w') as file:
            file.write(value)
            return True
    except Exception:
        logger.exception(
            f"An unexpected error occurred while writing to file:"
            f" {PREVIOUS_VALUE_FILE}"
        )
