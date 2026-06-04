from netmiko import ConnectHandler
import yaml

with open("inventory.yaml") as f:
    devices = yaml.safe_load(f)["devices"]

commands = [
    "router ospf 1",
    "passive-interface FastEthernet0/0"
]

for device in devices:

    print(f"Fixing {device['name']}")

    conn = ConnectHandler(
        host=device["host"],
        username=device["username"],
        password=device["password"],
        device_type=device["device_type"]
    )

    output = conn.send_config_set(commands)

    print(output)

    conn.save_config()

    conn.disconnect()