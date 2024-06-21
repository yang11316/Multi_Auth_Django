from django.db import models

# Create your models here.


class SoftwareTable(models.Model):
    software_id = models.CharField(
        max_length=32, primary_key=True, verbose_name="software_id"
    )
    user_id = models.ForeignKey(
        to="usermanage.UserTable",
        to_field="user_id",
        on_delete=models.CASCADE,
        verbose_name="user id",
    )
    software_version = models.CharField(max_length=50, verbose_name="software version")
    software_name = models.CharField(max_length=20, verbose_name="software name")
    software_hash = models.CharField(max_length=32, verbose_name="software hash")
    software_desc = models.TextField(verbose_name="software descryption", null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="create time")
    update_time = models.DateTimeField(auto_now=True, verbose_name="update time")

    def get_data(self):
        return {
            "software_id": self.software_id,
            "user_id": self.user_id.user_id,
            "software_version": self.software_version,
            "software_name": self.software_name,
            "software_hash": self.software_hash,
            "software_desc": self.software_desc,
            "create_time": self.create_time,
            "update_time": self.update_time,
        }


# 暂时无用
class SoftwareLocation(models.Model):
    softwarelocation_index = models.AutoField(
        primary_key=True, verbose_name="software index"
    )
    software_id = models.ForeignKey(
        to="softwaremanage.SoftwareTable",
        to_field="software_id",
        on_delete=models.CASCADE,
        verbose_name="software id",
    )
    node_ip = models.CharField(max_length=15, verbose_name="node ip")
    entity_ip = models.CharField(max_length=15, verbose_name="entity ip")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="create time")
    update_time = models.DateTimeField(auto_now=True, verbose_name="update time")


class RegisterSoftwareTable(models.Model):
    rsoftware_id = models.CharField(
        max_length=32, primary_key=True, verbose_name="rsoftware_id"
    )
    rsoftware_name = models.CharField(max_length=20, verbose_name="rsoftware name")
    rsoftware_path = models.CharField(max_length=50, verbose_name="rsoftware path")
    rsoftware_version = models.CharField(
        max_length=50, verbose_name="rsoftware version"
    )
    user_id = models.ForeignKey(
        to="usermanage.UserTable",
        to_field="user_id",
        on_delete=models.CASCADE,
        verbose_name="user id",
    )
    rsoftware_desc = models.TextField(verbose_name="rsoftware descryption", null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="create time")
    update_time = models.DateTimeField(auto_now=True, verbose_name="update time")

    def get_data(self):
        return {
            "rsoftware_id": self.rsoftware_id,
            "rsoftware_name": self.rsoftware_name,
            "rsoftware_path": self.rsoftware_path,
            "rsoftware_version": self.rsoftware_version,
            "user_id": self.user_id.user_id,
            "rsoftware_desc": self.rsoftware_desc,
            "create_time": self.create_time,
        }


class RegisterSoftwareLocationTable(models.Model):
    rlsoftwarelocation_index = models.AutoField(
        primary_key=True, verbose_name="rsoftware index"
    )
    rsoftware_id = models.ForeignKey(
        to="softwaremanage.RegisterSoftwareTable",
        to_field="rsoftware_id",
        on_delete=models.CASCADE,
        verbose_name="rsoftware id",
    )
    node_ip = models.GenericIPAddressField(verbose_name="node ip")
    entity_ip = models.GenericIPAddressField(verbose_name="entity ip")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="create time")
    update_time = models.DateTimeField(auto_now=True, verbose_name="update time")

    def get_data(self):
        return {
            "rsoftware_id": self.rsoftware_id.rsoftware_id,
            "node_ip": self.node_ip,
            "entity_ip": self.entity_ip,
            "create_time": self.create_time,
        }
