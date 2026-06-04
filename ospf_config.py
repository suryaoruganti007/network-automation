from netmiko import ConnectHandler
import yaml

with open("inventory.yaml") as f:
    devices = yaml.safe_load(f)["devices"]

commands = [
    "router ospf 1",
    "network 10.0.0.0 0.255.255.255 area 0",
    "network 192.168.84.0 0.0.0.255 area 0"
]

for device in devices:

    print(f"Configuring OSPF on {device['name']}")

    conn = ConnectHandler(
        host=device["host"],
        username=device["username"],
        password=device["password"],
        device_type=device["device_type"]
    )

    output = conn.send_config_set(commands)

    conn.save_config()

    conn.disconnect()

    print("Done")