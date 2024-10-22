# Public IP Tracker with YAML Update

This program works in conjunction with [public_ip_tracker](https://github.com/NemanjaSlijepcevic/public_ip_tracker), developed by me. It tracks the server's public IP address, compares it with the previously stored value, and updates a YAML configuration file if the IP changes. Additionally, it logs events and can integrate with an API for external access.

## Features

- Periodically checks the server's public IP address.
- Updates the IP address in a YAML file under the `sourceRange` field.
- Supports logging of application activity, both to a file and to standard output.
- Runs continuously, checking the IP every 60 seconds.

## How It Works

1. **Fetch the Current IP**: The program fetches the current public IP address using an API endpoint (`NODE_IP_DOMAIN`) secured with a Bearer token (`API_IP_TOKEN`).
2. **Compare with Previous IP**: It reads the previously stored IP from `current_ip.txt`. If the IP has changed, it updates the `sourceRange` list in the specified YAML file (`yaml_file.txt`).
3. **Update YAML File**: If the IP has changed, it replaces the old IP or appends the new one to the `sourceRange` list in the YAML file.
4. **Log Activities**: All actions are logged, and any errors or HTTP failures are reported.

## Configuration

### Environment Variables

To configure this program, the following environment variables are required:

- **NODE_IP_DOMAIN**: The API URL to fetch the current IP address.
- **API_IP_TOKEN**: The Bearer token for authenticating API requests.
- **LOG_LEVEL**: The level of logging. Defaults to `INFO`.
- **TARGET_FILE**: Path to the YAML file where the IP address will be updated.
  
### Files

- **current_ip.txt**: Stores the previous public IP address.
- **yaml_file.txt**: The YAML file containing the `sourceRange` list for updating the IP.

## Setup

1. Clone this repository and navigate to the project directory.

~~~bash
git clone https://github.com/NemanjaSlijepcevic/public_ip_tracker_yaml.git
cd public_ip_tracker_yaml
~~~

2. Install the required dependencies.

~~~bash
pip install -r requirements.txt
~~~

3. Set the required environment variables:

~~~bash
export NODE_IP_DOMAIN="https://your-api-domain.com/api/ip"
export API_IP_TOKEN="your-api-token"
export TARGET_FILE="path/to/your/yaml_file.txt"
export LOG_LEVEL="DEBUG"  # Optional, defaults to INFO
~~~

4. Run the program:

~~~bash
python main.py
~~~

## Logs

The program writes logs to both a log file (`app.log`) and the console. The default log level is `INFO`, but you can configure this using the `LOG_LEVEL` environment variable.

## Error Handling

- **API Failures**: If the API request fails, it will log an error and retry in the next loop.
- **File Read/Write Errors**: If there are issues with reading the `current_ip.txt` or `yaml_file.txt`, they are logged with details, and the program will continue to run.
