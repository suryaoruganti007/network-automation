from netmiko import ConnectHandler
from datetime import datetime
from logging_config import logger
import yaml
import os

os.makedirs(
    "backups",
    exist_ok=True
)

with open("inventory.yaml") as f:
    devices = yaml.safe_load(f)["devices"]

for device in devices:

    try:

        logger.info(
            f"Starting backup for "
            f"{device['name']}"
        )

        conn = ConnectHandler(
            host=device["host"],
            username=device["username"],
            password=device["password"],
            device_type=device["device_type"]
        )

        config = conn.send_command(
            "show running-config"
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = (
            f"backups/"
            f"{device['name']}_{timestamp}.txt"
        )

        with open(
            filename,
            "w"
        ) as file:

            file.write(config)

        conn.disconnect()

        print(
            f"Backup saved: {filename}"
        )

        logger.info(
            f"Backup successful "
            f"{filename}"
        )

    except Exception as e:

        logger.error(
            f"Backup failed for "
            f"{device['name']} : {e}"
        )