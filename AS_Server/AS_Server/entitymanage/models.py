from django.db import models


# Create your models here.
class EnityTable(models.Model):
    entity_index = models.AutoField(primary_key=True, verbose_name="entity index")
    entity_pid = models.CharField(max_length=32, verbose_name="entity pid")
    software_name = models.CharField(max_length=20, verbose_name="software name")
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
    entity_listening_port = models.IntegerField(
        verbose_name="entity listening port",
        null=True,
    )
    entity_sending_port = models.IntegerField(
        verbose_name="entity sending port",
        null=True,
    )
    entity_ip = models.GenericIPAddressField(verbose_name="entity ip")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="create time")
    update_time = models.DateTimeField(auto_now=True, verbose_name="update time")
    is_alive = models.BooleanField(default=False, verbose_name="entity alive")

    def get_data(self):
        return {
            "entity_pid": self.entity_pid,
            "software_id": self.software_id.software_id,
            "software_name": self.software_name,
            "user_id": self.user_id.user_id,
            "node_id": self.node_id.node_id,
            "entity_parcialkey": self.entity_parcialkey,
            "entity_porecessid": self.entity_porecessid,
            "entity_ip": self.entity_ip,
            "is_alive": self.is_alive,
            "create_time": self.create_time,
            "update_time": self.update_time,
        }


class KGCParamterTable(models.Model):
    kgc_id = models.CharField(primary_key=True, max_length=32, verbose_name="kgc id")
    kgc_s = models.TextField(verbose_name="kgc s")
    kgc_Ppub = models.TextField(verbose_name="kgc Ppub")
    kgc_q = models.TextField(verbose_name="kgc q")
    kgc_acc_G = models.TextField(verbose_name="kgc acc G")
    kgc_acc_publickey = models.TextField(verbose_name="kgc acc public key")
    kgc_acc_cur = models.TextField(verbose_name="kgc acc cur")
    kgc_acc_serectkey0 = models.TextField(verbose_name="kgc acc serect key 0")
    kgc_acc_serectkey1 = models.TextField(verbose_name="kgc acc serect key 1")
