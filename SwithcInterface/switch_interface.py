

class RFACPacket:
    def __init__(self,code=0, packet_id=0, sid=0) -> None:
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
            raise ValueError(f"Value length must be {expected_length} bytes for type {tlv_type}")
        self.fields[tlv_type] = value    
    def set_ip(self, tlv_type, ip_address):
        """
        设置 IP 地址字段
        :param tlv_type: TLV 类型(1: Source IP, 4: Destination IP)
        :param ip_address: 字符串形式的 IP 地址(如 "192.168.0.1")
        """
        parts = map(int, ip_address.split('.'))
        self.set_field(tlv_type, bytes(parts))
    def set_mask(self, tlv_type, mask):
        """
        设置 IP 地址字段
        :param tlv_type: TLV 类型(1: Source IP, 4: Destination IP)
        :param ip_address: 字符串形式的 IP 地址(如 "192.168.0.1")
        """
        parts = map(int, mask.split('.'))
        self.set_field(tlv_type, bytes(parts))
    def set_mac(self, tlv_type, mac_address):
        """
        设置 MAC 地址字段
        :param tlv_type: TLV 类型（8 或 9）
        :param mac_address: MAC 地址（字符串格式，如 '00:1A:2B:3C:4D:5E'）
        """
        try:
            mac_bytes = bytes(int(b, 16) for b in mac_address.split(':'))
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

if __name__ == "__main__":
    rfac_packet = RFACPacket(code=1, packet_id=1, sid=1)
    rfac_packet.set_ip(1, "192.168.3.11")
    rfac_packet.set_port(2, 53805)
    rfac_packet.set_mask(3, "255.255.255.255")
    rfac_packet.set_ip(4, "239.255.0.1")
    rfac_packet.set_port(5, 7900)
    rfac_packet.set_mask(6, "255.255.255.255")
    rfac_packet.set_protocol(17)
    rfac_packet.set_mac(8, "00:1A:2B:3C:4D:5E")
    rfac_packet.set_mac(9, "00:1A:2B:3C:4D:5E")
    print(rfac_packet.build())
