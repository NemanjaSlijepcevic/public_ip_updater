The text is clear, informative, and well-structured, but there are a few minor corrections needed, especially for typos and file paths. Here's an improved version:

---

# Public IP Tracker with YAML Update

This program works in conjunction with [public_ip_tracker](https://github.com/NemanjaSlijepcevic/public_ip_tracker), developed by me. It tracks the server's public IP address, compares it with the previously stored value, and updates a YAML configuration file if the IP changes. Additionally, it logs events and can integrate with an API for external access. By default, the app works with Traefik's white IP address rule file.

## Features

- Periodically checks the server's public IP address.
- Updates the IP address in a YAML file under the defined field.
- Supports logging of application activity, both to a file and to standard output.
- Runs continuously, checking the IP every 60 seconds.

## How It Works

1. **Fetch the Current IP**: The program fetches the current public IP address using an API endpoint (`NODE_IP_DOMAIN`) secured with a Bearer token (`API_IP_TOKEN`).
2. **Compare with Previous IP**: It reads the previously stored IP from `current_ip.txt`. If the IP has changed, it updates the `specified_file_path` list in the specified YAML file (`configuration.yml`).
3. **Update YAML File**: If the IP has changed, it replaces the old IP or appends the new one to the `specified_file_path` list in the YAML file.
4. **Log Activities**: All actions are logged, and any errors or HTTP failures are reported.

## Configuration

### Environment Variables

To configure this program, the following environment variables are required:

- **NODE_IP_DOMAIN**: The API URL to fetch the current IP address.
- **API_IP_TOKEN**: The Bearer token for authenticating API requests.
- **LOG_LEVEL**: The level of logging. Defaults to `INFO`.
- **CHECK_FREQUENCY**: Task execution frequency in seconds (default: `60`).
- **FILE_DATA_PATH**: Path to the data in the YAML file (default: `http.middlewares.default-whitelist.ipAllowList.sourceRange`).

### Files

- **current_ip.txt**: Stores the previous public IP address.
- **configuration.yml**: The YAML file containing the `specified_file_path` list for updating the IP.

## Setup

1. Clone this repository and navigate to the project directory:

```bash
git clone https://github.com/NemanjaSlijepcevic/public_ip_updater.git
cd public_ip_updater
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with the required environment variables:

```env
NODE_IP_DOMAIN="https://your-api-domain.com/api/ip"
API_IP_TOKEN="your-api-token"
LOG_LEVEL="DEBUG"  # Optional, defaults to INFO
CHECK_FREQUENCY=60  # Optional, defaults to 60
FILE_DATA_PATH="file.path.to.the.variable"  # Optional, default: `http.middlewares.default-whitelist.ipAllowList.sourceRange`.
```

4. Run the program:

```bash
python main.py
```

## Docker

You can run the application in a Docker container using the provided `Dockerfile`. The latest Docker image for this application is available at **`nemanjaslijepcevic/public_ip_updater:latest`**.

### Using Pre-Built Docker Image

1. **Pull the latest image** from GitHub Container Registry (GHCR):

```bash
docker pull nemanjaslijepcevic/public_ip_updater:latest
```

2. **Run the Docker container**:

```bash
docker run -d \
  --name public_ip_updater \
  -e NODE_IP_DOMAIN="https://your-api-domain.com/api/ip" \
  -e FILE_DATA_PATH="file.path.to.the.variable" \
  -e API_IP_TOKEN="api_token" \
  -e TZ="Europe/Belgrade" \
  -e LOG_LEVEL="DEBUG" \
  -v /path/to/public_ip_updater/current_ip.txt:/app/current_ip.txt:rw \
  -v /path/to/yaml/you/need/to/update.yml:/app/configuration.yml:rw \
  --restart unless-stopped \
  nemanja_slijepcevic/public_ip_updater
```

### Docker Compose

For easier management of Docker containers and environment configuration, you can use **Docker Compose**.

1. Create a `docker-compose.yml` file in the root of your project:

```yaml
version: '3'

services:
  public_ip_updater:
    image: nemanja_slijepcevic/public_ip_updater
    container_name: public_ip_updater
    environment:
      NODE_IP_DOMAIN: "https://your-api-domain.com/api/ip"
      FILE_DATA_PATH: "file.path.to.the.variable"
      API_IP_TOKEN: "api_token"
      TZ: "Europe/Belgrade"
      LOG_LEVEL: "DEBUG"
    volumes:
      - /path/to/public_ip_updater/current_ip.txt:/app/current_ip.txt:rw
      - /path/to/yaml/you/need/to/update.yml:/app/configuration.yml:rw
    restart: unless-stopped
```

2. **Build and run with Docker Compose**:

```bash
docker-compose up --build -d
```

3. **Stopping the app**:

```bash
docker-compose down
```

## Running Tests

You can run the unit tests using `pytest`. If you have Docker configured for testing, you can use it as well.

1. **Run tests locally**:

```bash
pytest
```

## Logs

The program writes logs to both a log file (`app.log`) and the console. The default log level is `INFO`, but you can configure this using the `LOG_LEVEL` environment variable.

## Error Handling

- **API Failures**: If the API request fails, it will log an error and retry in the next loop.
- **File Read/Write Errors**: If there are issues with reading `current_ip.txt` or `configuration.yml`, they are logged with details, and the program will continue to run.

---

### Corrections:
- Fixed a typo: `configuartion.yml` → `configuration.yml`.
- Updated example commands and file paths to be more consistent.
- Clarified the default value for `FILE_DATA_PATH`.
