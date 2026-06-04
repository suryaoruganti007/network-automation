from netmiko import ConnectHandler
from logging_config import logger
import yaml
import difflib
import os

# Load inventory
with open("inventory.yaml") as f:
    devices = yaml.safe_load(f)["devices"]

# Lines that should not be considered drift
skip_patterns = [
    "Last configuration change",
    "Current configuration"
]

for device in devices:

    print(f"\nChecking {device['name']}...")

    logger.info(
        f"Starting drift check for {device['name']}"
    )

    try:

        # Connect to router
        conn = ConnectHandler(
            host=device["host"],
            username=device["username"],
            password=device["password"],
            device_type=device["device_type"]
        )

        # Get running config
        running = conn.send_command(
            "show running-config"
        )

        conn.disconnect()

    except Exception as e:

        print(
            f"Connection failed: {device['name']}"
        )

        logger.error(
            f"Connection failed for "
            f"{device['name']} : {e}"
        )

        continue

    # Intended config location
    intended_path = (
        f"configs/{device['name']}_intended.txt"
    )

    # Verify intended config exists
    if not os.path.exists(intended_path):

        print(
            f"No intended config found for "
            f"{device['name']}"
        )

        logger.warning(
            f"Missing intended config for "
            f"{device['name']}"
        )

        continue

    # Read intended config
    with open(
        intended_path,
        "r"
    ) as f:

        intended = f.readlines()

    # Split running config into lines
    running_lines = running.splitlines()

    # Remove dynamic lines
    intended = [
        line.rstrip()
        for line in intended
        if not any(
            pattern in line
            for pattern in skip_patterns
        )
    ]

    running_lines = [
        line.rstrip()
        for line in running_lines
        if not any(
            pattern in line
            for pattern in skip_patterns
        )
    ]

    # Compare configurations
    diff = list(
        difflib.unified_diff(
            intended,
            running_lines,
            fromfile="intended",
            tofile="running",
            lineterm=""
        )
    )

    # Drift found
    if diff:

        print(
            f"\nDRIFT DETECTED: "
            f"{device['name']}"
        )

        print("-" * 60)

        print(
            "\n".join(
                diff[:50]
            )
        )

        print("-" * 60)

        logger.warning(
            f"Drift detected on "
            f"{device['name']}"
        )

    # No drift
    else:

        print(
            f"OK: {device['name']} "
            f"matches intended configuration"
        )

        logger.info(
            f"No drift detected on "
            f"{device['name']}"
        )

logger.info(
    "Drift detection run completed"
)