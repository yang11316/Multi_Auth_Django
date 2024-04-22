from django.db import models


# Create your models here.
class NodeTable(models.Model):
    node_id = models.CharField(max_length=32, primary_key=True, verbose_name="node id")
    node_ip = models.IPAddressField(verbose_name="node ip")
    node_port = models.IntegerField(verbose_name="node port")
    node_desc = models.TextField(verbose_name="node descryption", null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="create time")
    update_time = models.DateTimeField(auto_now=True, verbose_name="update time")

    def get_data(self):
        return {
            "node_id": self.node_id,
            "node_ip": self.node_ip,
            "node_port": self.node_port,
            "node_desc": self.node_desc,
        }


class LogTable(models.Model):
    log_id = models.CharField(max_length=32, primary_key=True, verbose_name="log id")
    log_node = models.ForeignKey(
        to="NodeTable",
        to_field="node_id",
        on_delete=models.CASCADE,
        verbose_name="log node",
    )
    log_type = models.CharField(max_length=20, verbose_name="log type")
    log_desc = models.TextField(verbose_name="log descryption", null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="create time")
