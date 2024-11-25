from django.db import models

# Create your models here.


"""
存储实体发送的dds会话信息 

dds type指定信息的类型：
1、publisher 0：向组ip发送消息
2、subscriber 1：接收组ip的消息
"""


class DDSInfoTable(models.Model):
    entity_pid = models.CharField(
        primary_key=True, max_length=32, verbose_name="entity pid"
    )
    dds_type = models.IntegerField(verbose_name="dds type")
    source_ip = models.GenericIPAddressField(verbose_name="source ip")
    source_port = models.IntegerField(verbose_name="source port")
    destination_ip = models.GenericIPAddressField(verbose_name="destination ip")
    destination_port = models.IntegerField(verbose_name="destination port")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="create time")
    update_time = models.DateTimeField(auto_now=True, verbose_name="update time")
