# public_ip_whitelister
This project works with public_ip_tracker to track changes in your public IP and update a YAML config file. It compares the current IP from the public_ip_tracker API with the last recorded IP and modifies the specified sourceRange if needed. The app is configurable via environment variables, ideal for managing IP whitelists automatically.
