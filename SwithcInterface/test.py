# from scapy.all import Ether, Raw, sendp, get_if_hwaddr

class RFACPacket:
    def __init__(self, code, packet_id, sid, data=None):
        """
        初始化 RFACPacket
        :param code: 报文类型（1字节）
        :param packet_id: 用于匹配响应的 ID（1字节）
        :param sid: Service ID（1字节）
        :param data: TLV 格式的数据列表
        """
        self.code = code
        self.packet_id = packet_id
        self.sid = sid
        self.data = data or []

    def add_tlv(self, tlv_type, value):
        """
        添加一个 TLV 格式的数据项
        :param tlv_type: 类型字段 (2 bytes)
        :param value: Value 数据
        """
        length = len(value)
        self.data.append({
            "type": tlv_type,
            "len": length,
            "value": value
        })

    def build(self):
        """
        构建报文
        :return: 报文的字节流
        """
        packet = [self.code, self.packet_id, self.sid]
        # Length 字段，计算 Data 的总长度
        total_length = sum(4 + len(field["value"]) for field in self.data)
        packet.extend(total_length.to_bytes(2, byteorder="big"))

        # 构建 Data 部分
        for field in self.data:
            packet.extend(field["type"].to_bytes(2, byteorder="big"))
            packet.extend(field["len"].to_bytes(2, byteorder="big"))
            packet.extend(field["value"])
        return bytes(packet)

    @staticmethod
    def parse(raw_data):
        """
        从原始字节流解析报文
        :param raw_data: 原始报文字节流
        :return: 解析后的 RFACPacket 对象
        """
        code = raw_data[0]
        packet_id = raw_data[1]
        sid = raw_data[2]
        length = int.from_bytes(raw_data[3:5], byteorder="big")
        data_fields = []
        index = 5

        while index < 5 + length:
            tlv_type = int.from_bytes(raw_data[index:index+2], byteorder="big")
            tlv_len = int.from_bytes(raw_data[index+2:index+4], byteorder="big")
            value = raw_data[index+4:index+4+tlv_len]
            data_fields.append({
                "type": tlv_type,
                "len": tlv_len,
                "value": value
            })
            index += 4 + tlv_len

        return RFACPacket(code, packet_id, sid, data_fields)

    def __repr__(self):
        return f"RFACPacket(code={self.code}, packet_id={self.packet_id}, sid={self.sid}, data={self.data})"

# 示例：构造 RFAC 报文
rfac_packet = RFACPacket(code=1, packet_id=1, sid=0x01)
rfac_packet.add_tlv(tlv_type=1, value=b'\xC0\xA8\x01\x01')  # Source IP: 192.168.1.1
rfac_packet.add_tlv(tlv_type=2, value=b'\x1F\x90')  # Source Port: 8080
rfac_packet.add_tlv(tlv_type=4, value=b'\xC0\xA8\x01\x02')  # Destination IP: 192.168.1.2
raw_data = rfac_packet.build()
print(raw_data)
# 示例：解析 RFAC 报文
parsed_packet = RFACPacket.parse(raw_data)
print(parsed_packet)

# 示例：发送报文
"""def send_packet(intf, raw_packet, num):
    src_mac = get_if_hwaddr(intf)
    ether_frame = Ether(src=src_mac, dst="01:80:c2:00:00:0f", type=0x8890) / Raw(raw_packet)
    sendp(ether_frame, iface=intf, count=num)
"""

# 调用发送函数
# send_packet("eth0", raw_data, 1)
