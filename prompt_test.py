from netmiko import ConnectHandler

conn = ConnectHandler(
    host="192.168.84.10",
    username="admin",
    password="cisco123",
    device_type="cisco_ios"
)

print(conn.find_prompt())

conn.disconnect()