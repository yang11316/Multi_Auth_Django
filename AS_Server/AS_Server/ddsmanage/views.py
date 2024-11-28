from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import DDSInfoTable, PacketID
from entitymanage.models import EnityTable
from commonutils import switch_interface
from django.conf import settings
from django.utils import timezone
import json
import requests
import threading


# Create your views here.


# 接收AP发来的实体的dds信息,保存并发送给交换机
def get_dds_info(request):
    if request.method == "POST":
        try:
            # 获取请求数据并解析
            json_data = request.body.decode("utf-8")
            json_data = json.loads(json_data)

            # 检查pid是否存在
            entity_pid = json_data.get("entity_pid")
            if not entity_pid:
                return JsonResponse(
                    {"status": "error", "message": "entity_pid is required"}
                )
            if not EnityTable.objects.filter(entity_pid=entity_pid).exists():
                return JsonResponse(
                    {"status": "error", "message": "entity_pid does not exist"}
                )
            # 检查dds信息是否完整
            validator = switch_interface.RequestDataValidator(json_data)
            validation_errors = validator.validate()
            if validation_errors:
                return JsonResponse(
                    {"status": "error", "message": ", ".join(validation_errors)}
                )

            # 数据校验完毕，保存到数据库中
            dds_info_instance = DDSInfoTable()
            dds_info_instance.entity_pid = entity_pid
            dds_info_instance.dds_type = json_data.get("dds_type")
            dds_info_instance.protocol_type = json_data.get("protocol_type")
            dds_info_instance.source_ip = json_data.get("source_ip")
            dds_info_instance.source_port = json_data.get("source_port")
            dds_info_instance.source_mask = json_data.get("source_mask")
            dds_info_instance.source_mac = json_data.get("source_mac")
            dds_info_instance.destination_ip = json_data.get("destination_ip")
            dds_info_instance.destination_port = json_data.get("destination_port")
            dds_info_instance.destination_mask = json_data.get("destination_mask")
            dds_info_instance.destination_mac = json_data.get("destination_mac")
            dds_info_instance.create_time = timezone.now()
            dds_info_instance.update_time = dds_info_instance.create_time

            dds_type = json_data.get("dds_type")
            protocol_type = json_data.get("protocol_type")
            source_ip = json_data.get("source_ip")
            source_port = json_data.get("source_port")
            source_mask = json_data.get("source_mask")
            source_mac = json_data.get("source_mac")
            destination_ip = json_data.get("destination_ip")
            destination_port = json_data.get("destination_port")
            destination_mask = json_data.get("destination_mask")
            destination_mac = json_data.get("destination_mac")
            # code : 1 permit  packet_id : 递增 sid : 1
            rfac_packet = switch_interface.RFACPacket(
                code=1,
                packet_id=PacketID.get_next_id(),
                sid=1,
            )
            # 构造RFAC报文
            # 设置protocol值  dds_type: 1 publisher 2 subscriber   protocol_type: 1tcp  2udp
            if dds_type == 1:
                if protocol_type == 1:
                    rfac_packet.set_protocol(6)
                elif protocol_type == 2:
                    rfac_packet.set_protocol(17)
            else:
                rfac_packet.set_protocol(2)

            rfac_packet.set_ip(1, source_ip)
            rfac_packet.set_port(2, source_port)
            rfac_packet.set_mask(3, source_mask)
            rfac_packet.set_ip(4, destination_ip)
            rfac_packet.set_port(5, destination_port)
            rfac_packet.set_mask(6, destination_mask)
            rfac_packet.set_mac(8, source_mac)
            rfac_packet.set_mac(9, destination_mac)
            pack_data = rfac_packet.build()
            switch_interface.send_raw_packet(pack_data, settings.SWITHCH_MAC)
            dds_info_instance.save()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


# 接收撤销的消息，删除并发送给交换机
def get_dds_info_delete(request):
    if request.method == "POST":
        json_data = request.body.decode("utf-8")
        json_data = json.loads(json_data)
        entity_pid = json_data.get("entity_pid")
        if not entity_pid:
            return JsonResponse(
                {"status": "error", "message": "entity_pid is required"}
            )
        if not EnityTable.objects.filter(entity_pid=entity_pid).exists():
            return JsonResponse(
                {"status": "error", "message": "entity_pid does not exist"}
            )
