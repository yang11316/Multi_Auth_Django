
import socket
import re

# 检查 IP 地址格式是否正确
def is_valid_ip(ip):

    try:
        socket.inet_aton(ip)  # 使用 socket 库来检查 IP 是否有效
        return True
    except socket.error:
        return False


# 检查端口号是否在有效范围内(0-65535)
def is_valid_port(port):

    return 0 <= port <= 65535


# 检查 IP 地址掩码格式是否正确
def is_valid_mask(mask):
    """
    校验 IP 地址掩码格式，确保是四个 0 到 255 的数字，用点分隔。
    例如: "255.255.255.0"
    """
    # 使用正则表达式检查格式是否符合
    if re.match(r"^(\d{1,3}\.){3}\d{1,3}$", mask):
        # 检查每个部分的值是否在 0 到 255 之间
        octets = mask.split(".")
        return all(0 <= int(octet) <= 255 for octet in octets)
    return False


# 检查 MAC 地址格式是否正确
def is_valid_mac(mac):
    """
    校验 MAC 地址格式，确保是六个 2 位十六进制数，用冒号或连字符分隔。
    例如: "00:1A:2B:3C:4D:5E" 或 "00-1A-2B-3C-4D-5E"
    """
    # 检查是否符合正则表达式格式
    return bool(re.match(r"^([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$", mac))



# 校验输入的数据是否正确
class RequestDataValidator:
    def __init__(self, data):
        self.data = data
        self.errors = []

    def check_field(self, field, required=True, validator=None, valid_values=None):
        value = self.data.get(field)
        if required and not value:
            self.errors.append(f"{field} is required")
        elif validator and value and not validator(value):
            self.errors.append(f"Invalid {field} format")
        elif valid_values and value not in valid_values:
            self.errors.append(
                f"Invalid value for {field}. Allowed values: {valid_values}"
            )

    def validate(self):
        # Perform field checks and validations
        self.check_field("dds_type", required=True, valid_values=[1,2])
        self.check_field("protocol_type", required=True, valid_values=[1,2])

        self.check_field("source_ip", required=True, validator=is_valid_ip)
        self.check_field("source_port", required=True, validator=is_valid_port)

        # 校验 source_mask 和 source_mac
        self.check_field("source_mask", required=False, validator=is_valid_mask)
        self.check_field("source_mac", required=False, validator=is_valid_mac)

        self.check_field("destination_ip", required=True, validator=is_valid_ip)
        self.check_field("destination_port", required=True, validator=is_valid_port)

        # 校验 destination_mask 和 destination_mac
        self.check_field("destination_mask", required=False, validator=is_valid_mask)
        self.check_field("destination_mac", required=False, validator=is_valid_mac)

        return self.errors

