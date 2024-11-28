from django.db import models, transaction

# Create your models here.


"""
存储实体发送的dds会话信息 

dds type指定信息的类型
1、publisher 1:向组ip发送消息
2、subscriber 2:接收组ip的消息

protocol type指定信息的传输协议
1、tcp :1
2、udp :2

"""


class DDSInfoTable(models.Model):
    entity_pid = models.CharField(
        primary_key=True, max_length=32, verbose_name="entity pid"
    )
    dds_type = models.IntegerField(verbose_name="dds type")
    protocol_type = models.IntegerField(verbose_name="protocol type")
    source_ip = models.GenericIPAddressField(verbose_name="source ip")
    source_port = models.IntegerField(verbose_name="source port")
    source_mask = models.CharField(
        max_length=15, verbose_name="source mask", default="255.255.255.255"
    )
    source_mac = models.CharField(
        max_length=17, verbose_name="source mac", default="00:00:00:00:00:00"
    )
    destination_ip = models.GenericIPAddressField(verbose_name="destination ip")
    destination_port = models.IntegerField(verbose_name="destination port")
    destination_mask = models.CharField(
        max_length=15, verbose_name="destination mask", default="255.255.255.255"
    )
    destination_mac = models.CharField(
        max_length=17, verbose_name="destination mac", default="00:00:00:00:00:00"
    )

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="create time")
    update_time = models.DateTimeField(auto_now=True, verbose_name="update time")


class PacketID(models.Model):
    # id 字段为主键，固定值为1，保证表中只有一条记录
    id = models.IntegerField(primary_key=True, default=1)
    last_id = models.IntegerField(default=0)

    @classmethod
    def get_next_id(cls):
        """
        获取下一个 ID,ID 会在 0 到 255 之间递增并循环。
        """
        with transaction.atomic():
            obj, created = cls.objects.select_for_update().get_or_create(id=1)
            obj.last_id = (
                obj.last_id + 1
            ) % 256  # 每次递增后对 256 取余，确保 ID 在 0 到 255 之间
            obj.save()
            return obj.last_id
