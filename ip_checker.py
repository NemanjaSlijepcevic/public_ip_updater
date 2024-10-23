import os
import requests
import logging


# Constants from environment variables
API_URL = os.getenv('NODE_IP_DOMAIN')
BEARER_TOKEN = os.getenv('API_IP_TOKEN')
logger = logging.getLogger(__name__)


# Function to get data from the API
def get_current_value():
    try:
        headers = {
            'Authorization': f'Bearer {BEARER_TOKEN}'
        }
        logger.debug(f"Making GET request to: {API_URL}")
        response = requests.get(API_URL, headers=headers)
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        logger.debug(f"Response content: {response.text}")
        response.raise_for_status()
        data = response.json()
        ip_address = data.get("ip")  # Extract the "ip" field

        if not ip_address:
            logger.error("IP address not found in the API response.")
            return None

        return ip_address
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}", exc_info=True)
    except Exception:
        logger.exception(
            "An unexpected error occurred during GET request."
        )
        return None
