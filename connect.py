from netmiko import ConnectHandler
from logging_config import logger
import yaml

with open("inventory.yaml") as f:
    devices = yaml.safe_load(f)["devices"]

for device in devices:

    try:

        logger.info(
            f"Connecting to {device['name']}"
        )

        connection = ConnectHandler(
            host=device["host"],
            username=device["username"],
            password=device["password"],
            device_type=device["device_type"]
        )

        output = connection.send_command(
            "show ip interface brief"
        )

        print(
            f"\n===== {device['name']} ====="
        )

        print(output)

        connection.disconnect()

        logger.info(
            f"Successfully connected to {device['name']}"
        )

    except Exception as e:

        logger.error(
            f"Failed connection to "
            f"{device['name']} : {e}"
        )

        print(
            f"Failed to connect to "
            f"{device['name']}"
        )