from netmiko import ConnectHandler
from logging_config import logger
import yaml

with open("inventory.yaml") as f:
    devices = yaml.safe_load(f)["devices"]

commands = [
    "banner motd #Managed by Python Automation#"
]

for device in devices:

    try:

        logger.info(
            f"Pushing config to "
            f"{device['name']}"
        )

        conn = ConnectHandler(
            host=device["host"],
            username=device["username"],
            password=device["password"],
            device_type=device["device_type"]
        )

        output = conn.send_config_set(
            commands
        )

        print(output)

        conn.save_config()

        conn.disconnect()

        logger.info(
            f"Config push successful on "
            f"{device['name']}"
        )

    except Exception as e:

        logger.error(
            f"Config push failed on "
            f"{device['name']} : {e}"
        )