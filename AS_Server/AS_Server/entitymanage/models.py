from django.db import models


# Create your models here.
class EnityTable(models.Model):
    entity_index = models.AutoField(primary_key=True, verbose_name="entity index")
    entity_pid = models.CharField(max_length=32, verbose_name="entity pid")
    software_id = models.ForeignKey(
        to="softwaremanage.SoftwareTable",
        to_field="software_id",
        on_delete=models.CASCADE,
        verbose_name="software id",
    )
    user_id = models.ForeignKey(
        to="usermanage.UserTable",
        to_field="user_id",
        on_delete=models.CASCADE,
        verbose_name="user id",
    )
    node_id = models.ForeignKey(
        to="nodemanage.NodeTable",
        to_field="node_id",
        on_delete=models.CASCADE,
        verbose_name="node id",
    )
    entity_parcialkey = models.TextField(verbose_name="entity parcial key", null=True)
    entity_porecessid = models.CharField(
        max_length=20, verbose_name="entity process id", null=True
    )
    entity_port = models.IntegerField(
        verbose_name="entity port",
        null=True,
    )
    entity_ip = models.CharField(max_length=15, verbose_name="entity ip")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="create time")
    update_time = models.DateTimeField(auto_now=True, verbose_name="update time")
    is_alive = models.BooleanField(default=False, verbose_name="entity alive")

    def get_data(self):
        return {
            "entity_index": self.entity_index,
            "software_id": self.software_id.software_id,
            "user_id": self.user_id.user_id,
            "node_id": self.node_id.node_id,
            "entity_parcialkey": self.entity_parcialkey,
            "entity_porecessid": self.entity_porecessid,
            "entity_port": self.entity_port,
            "entity_ip": self.entity_ip,
            "create_time": self.create_time,
            "update_time": self.update_time,
            "is_alive": self.is_alive,
        }
