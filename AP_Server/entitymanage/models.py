from django.db import models

# Create your models here.

class EntityInfo(models.Model):
    entity_index = models.AutoField(primary_key=True,verbose_name="entity_name")
    entity_pid = models.CharField(max_length=32, verbose_name="entity pid")
    software_id = models.CharField(
        max_length=32,  verbose_name="software_id"
    )
    software_hash = models.CharField(max_length=32, verbose_name="software hash")
    user_id = models.CharField(max_length=32, verbose_name="user id")
    entity_parcialkey = models.TextField(verbose_name="entity parcial key", null=True)
    entity_porecessid = models.CharField(
        max_length=20, verbose_name="entity process id", null=True
    )
    entity_listening_port = models.IntegerField(verbose_name="entity listening port", null=True)
    entity_sending_port = models.IntegerField(verbose_name="entity sending port", null=True)
    entity_ip = models.CharField(max_length=15, verbose_name="entity ip")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="create time")
    update_time = models.DateTimeField(auto_now=True, verbose_name="update time")
    is_alive = models.BooleanField(default=False, verbose_name="entity alive")

    def get_data(self):
        return {
            "entity_index": self.entity_index,
            "entity_pid": self.entity_pid,
            "software_id": self.software_id,
            "user_id": self.user_id,
            "entity_parcialkey": self.entity_parcialkey,
            "entity_porecessid": self.entity_porecessid,
            "entity_listening_port": self.entity_listening_port,
            "entity_sending_port":self.entity_sending_port,
            "entity_ip": self.entity_ip,
            "create_time": self.create_time,
           "update_time": self.update_time,
           "is_alive": self.is_alive
       }

class PublicParamtersTable(models.Model):
    kgc_id = models.CharField(max_length=32, primary_key=True,verbose_name="kgc_id")
    acc_publickey = models.TextField(verbose_name="acc_publickey")
    acc_cur = models.TextField(verbose_name="acc_cur")
    kgc_q = models.TextField(verbose_name="kgc_q")
    kgc_Ppub = models.TextField(verbose_name="kgc_PpublicKey")
