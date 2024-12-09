from scapy.all import *
from scapy.layers.inet import *
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


# RFAC 报文类
class RFACPacket:
    def __init__(self, code=0, packet_id=0, sid=0) -> None:
        """
        初始化 RFACPacket
        :param code: 报文类型(1字节)
        :param packet_id: 用于匹配响应的 ID(1字节)
        :param sid: Service ID(1字节)
        :param data: TLV 格式的数据列表
        """
        self.code = code
        self.packet_id = packet_id
        self.sid = sid
        self.fields = {
            1: bytes(4),  # Source IP
            2: bytes(2),  # Source Port
            3: bytes(4),  # Source Mask
            4: bytes(4),  # Destination IP
            5: bytes(2),  # Destination Port
            6: bytes(4),  # Destination Mask
            7: bytes(1),  # Protocol
            8: bytes(6),  # Source Mac
            9: bytes(6),  # Destination Mac
        }

    def set_field(self, tlv_type, value):
        """
        设置指定 TLV 字段的值
        :param tlv_type: TLV 类型(Type 字段)
        :param value: 新的值(bytes 类型)
        """
        if tlv_type not in self.fields:
            raise ValueError(f"Invalid TLV type: {tlv_type}")
        expected_length = len(self.fields[tlv_type])
        if len(value) != expected_length:
            raise ValueError(
                f"Value length must be {expected_length} bytes for type {tlv_type}"
            )
        self.fields[tlv_type] = value

    def set_ip(self, tlv_type, ip_address):
        """
        设置 IP 地址字段
        :param tlv_type: TLV 类型(1: Source IP, 4: Destination IP)
        :param ip_address: 字符串形式的 IP 地址(如 "192.168.0.1")
        """
        parts = map(int, ip_address.split("."))
        self.set_field(tlv_type, bytes(parts))

    def set_mask(self, tlv_type, mask):
        """
        设置 IP 地址字段
        :param tlv_type: TLV 类型(1: Source IP, 4: Destination IP)
        :param ip_address: 字符串形式的 IP 地址(如 "192.168.0.1")
        """
        parts = map(int, mask.split("."))
        self.set_field(tlv_type, bytes(parts))

    def set_mac(self, tlv_type, mac_address):
        """
        设置 MAC 地址字段
        :param tlv_type: TLV 类型（8 或 9）
        :param mac_address: MAC 地址（字符串格式，如 '00:1A:2B:3C:4D:5E'）
        """
        mac_address = mac_address.replace("-", ":").upper()
        try:
            mac_bytes = bytes(int(b, 16) for b in mac_address.split(":"))
        except ValueError:
            raise ValueError("Invalid MAC address format")
        if len(mac_bytes) != 6:
            raise ValueError("MAC address must be 6 bytes")
        self.set_field(tlv_type, mac_bytes)

    def set_port(self, tlv_type, port):
        """
        设置端口字段
        :param tlv_type: TLV 类型(2: Source Port, 5: Destination Port)
        :param port: 整数形式的端口号
        """
        self.set_field(tlv_type, port.to_bytes(2, byteorder="big"))

    def set_protocol(self, protocol):
        """
        设置协议字段
        :param protocol: 协议号(整数,TCP 为 6,UDP 为 17 等)
        """
        self.set_field(7, protocol.to_bytes(1, byteorder="big"))

    def build(self):
        """
        构建报文
        :return: 报文的字节流
        """
        packet = [self.code, self.packet_id, self.sid]

        # Length 字段，计算 Data 的总长度
        total_length = sum(4 + len(value) for value in self.fields.values())
        packet.extend(total_length.to_bytes(2, byteorder="big"))

        # 构建 Data 部分
        for tlv_type, value in self.fields.items():
            packet.extend(tlv_type.to_bytes(2, byteorder="big"))
            packet.extend(len(value).to_bytes(2, byteorder="big"))
            packet.extend(value)
        return bytes(packet)


# 校验输入的数据是否正确
class RequestDataValidator:
    def __init__(self, data):
        self.data = data
        self.errors = []

    def check_field(self, field, required=True, validator=None, valid_values=None):
        value = self.data.get(field)
        if required and value is None:  # 检查是否为 None，而不是假值
            self.errors.append(f"{field} is required")
        elif (
            validator and value is not None and not validator(value)
        ):  # 仅在值非 None 时验证
            self.errors.append(f"Invalid {field} format")
        elif valid_values and value not in valid_values:
            self.errors.append(
                f"Invalid value for {field}. Allowed values: {valid_values}"
            )

    def validate(self):
        # Perform field checks and validations
        self.check_field("dds_type", required=True, valid_values=[1, 2])
        self.check_field("protocol_type", required=True, valid_values=[1, 2])

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


# 获取本地的默认网卡,以“ens”开头
def get_local_interface():
    interfaces = get_if_list()
    # 筛选以 "ens" 开头的接口
    ens_interfaces = [iface for iface in interfaces if iface.startswith("ens")]
    if ens_interfaces:
        # 选择第一个以 "ens" 开头的接口
        iface = ens_interfaces[0]
        return iface
    else:

        return None


# 获取指定网卡的mac地址
def get_mac_address(iface):
    return get_if_hwaddr(iface)


# 发送二层数据包，不接收返回消息 destination_mac为交换机的mac地址
def send_raw_packet(packet, destination_mac):
    def send_packet():
        iface = get_local_interface()
        if iface is None:
            print("No 'ens' interfaces found.")
            return
        print(f"Interface: {iface}")
        source_mac = get_mac_address(iface)
        print(f"Source MAC: {source_mac}")
        print(f"Destination MAC: {destination_mac}")

        pack = Ether(src=source_mac, dst=destination_mac, type=0x8890) / Raw(packet)
        sendp(pack, iface=iface, count=1)

        print("Packet sent successfully.")

    send_thread = threading.Thread(target=send_packet)
    send_thread.start()  # 异步启动线程


if __name__ == "__main__":
    data = '{"source_ip": "192.168.3.11"}'
    json_data = json.loads(data)
    validator = RequestDataValidator(json_data)
    errors = validator.validate()
    print(errors)

    rfac_packet = RFACPacket(code=1, packet_id=1, sid=1)
    rfac_packet.set_ip(1, "192.168.3.11")
    rfac_packet.set_port(2, 53805)
    rfac_packet.set_mask(3, "255.255.255.255")
    rfac_packet.set_ip(4, "239.255.0.1")
    rfac_packet.set_port(5, 0)
    rfac_packet.set_mask(6, "255.255.255.255")
    rfac_packet.set_protocol(17)
    rfac_packet.set_mac(8, "00:1A:2B:3C:4D:5E")
    rfac_packet.set_mac(9, "00:1A:2B:3C:4D:5E")
    data = rfac_packet.build()
    print(data)

    # interfaces = get_if_list()
    # # 筛选以 "ens" 开头的接口
    # ens_interfaces = [iface for iface in interfaces if iface.startswith("ens")]
    # if ens_interfaces:
    #     # 选择第一个以 "ens" 开头的接口
    #     iface = ens_interfaces[0]
    #     try:
    #         # 获取该接口的 MAC 地址
    #         mac_address = get_if_hwaddr(iface)

    #         print(f"Interface: {iface}, MAC Address: {mac_address}")
    #         p = Ether(dst="D2:D1:73:3B:84:35", type=0x8890) / Raw(data)
    #         # sendp(p, iface=iface)
    #         # ip = IP(dst="192.168.3.17", src="192.168.3.17")
    #         ans, unans = srp(
    #             p,
    #             iface=iface,
    #             timeout=1,
    #         )
    #         for snd, rcv in unans:
    #             print(rcv.show())
    #     except Exception as e:
    #         print(f"Could not retrieve MAC address for {iface}: {e}")
    # else:
    #     print("No 'ens' interfaces found.")
