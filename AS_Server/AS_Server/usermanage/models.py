from django.db import models


# Create your models here.
class ManagerTable(models.Model):
    manager_id = models.CharField(
        max_length=32, primary_key=True, verbose_name="manager id"
    )
    manager_name = models.CharField(max_length=20, verbose_name="manager name")
    manager_pwd = models.CharField(max_length=20, verbose_name="manager password")
    manager_phone = models.CharField(
        max_length=11, verbose_name="manager phone", null=True
    )
    manager_email = models.EmailField(verbose_name="manager email", null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="create time")
    update_time = models.DateTimeField(auto_now=True, verbose_name="update time")


class RegisterTable(models.Model):
    user_id = models.CharField(max_length=32, primary_key=True, verbose_name="user id")
    user_name = models.CharField(max_length=20, verbose_name="user name")
    user_pwd = models.CharField(max_length=20, verbose_name="user password")
    user_phone = models.CharField(max_length=11, verbose_name="user phone", null=True)
    user_email = models.EmailField(verbose_name="user email", null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="create time")
    update_time = models.DateTimeField(auto_now=True, verbose_name="update time")

    def get_data(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_phone": self.user_phone,
            "user_email": self.user_email,
            "create_time": self.create_time,
            "update_time": self.update_time,
        }


class UserTable(models.Model):
    user_id = models.CharField(max_length=32, primary_key=True, verbose_name="user id")
    user_name = models.CharField(max_length=20, verbose_name="user name")
    user_row = models.CharField(max_length=20, verbose_name="user row")
    user_pwd = models.CharField(max_length=16, verbose_name="user password")
    user_phone = models.CharField(max_length=11, verbose_name="user phone", null=True)
    user_email = models.EmailField(verbose_name="user email", null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="create time")
    update_time = models.DateTimeField(auto_now=True, verbose_name="update time")

    def get_data(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_row": self.user_row,
            "user_phone": self.user_phone,
            "user_email": self.user_email,
            "create_time": self.create_time,
            "update_time": self.update_time,
        }
