import os
import time
import logging
from yaml_utils import update_yaml_file
from ip_checker import get_current_value
from config_utils import check_inputs, check_frequency, check_and_create_file
from file_utils import read_previous_value, write_current_value


log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


check_inputs()
check_and_create_file()
frequency = check_frequency()


if __name__ == "__main__":
    logger.info("Starting public IP tracking app")
    while True:
        current_value = get_current_value()
        previous_value = read_previous_value()

        if current_value and current_value != previous_value:
            update_yaml_file(previous_value, current_value)
            write_current_value(current_value)
            logger.info(f"Value updated: {current_value}")
        else:
            logger.debug("No changes detected.")
        time.sleep(frequency)
