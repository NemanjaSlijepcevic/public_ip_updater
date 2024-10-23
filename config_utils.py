import os
import logging


logger = logging.getLogger(__name__)


# Check for necessary environment variables
def check_bearer_token():  # UT fails if this is checked without function
    BEARER_TOKEN = os.getenv('API_IP_TOKEN')
    if not BEARER_TOKEN:
        logger.error("BEARER_TOKEN is not set.")
        exit(1)
    return True  # unit testing check


def check_api_url():
    API_URL = os.getenv('NODE_IP_DOMAIN')
    if not API_URL:
        logger.error("NODE_IP_DOMAIN is not set.")
        exit(1)
    return True


def check_frequency():
    frequency = os.getenv('CHECK_FREQUENCY', '60')
    try:
        frequency = int(frequency)
    except ValueError:
        logger.error("Incorrect value of frequency.")
        exit(1)

    if frequency <= 1:
        logger.error("Incorrect value of frequency.")
        exit(1)

    return frequency


def check_file_data_path():
    FILE_DATA_PATH = os.getenv(
        'FILE_DATA_PATH',
        'http.middlewares.default-whitelist.ipAllowList.sourceRange'
    )

    if not isinstance(FILE_DATA_PATH, str) or len(FILE_DATA_PATH) <= 5:
        logger.error("Incorrect value of FILE_DATA_PATH.")
        exit(1)

    return True


def check_log_level():
    VALID_LOG_LEVELS = {
        "NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
    }
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    if log_level not in VALID_LOG_LEVELS:
        logger.error(f"Invalid log level: '{log_level}'.")
        exit(1)
    return True


def check_inputs():
    check_bearer_token()
    check_api_url()
    check_frequency()
    check_file_data_path()
    check_log_level()
    return True
