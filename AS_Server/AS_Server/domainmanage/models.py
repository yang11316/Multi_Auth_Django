from django.db import models


# Create your models here.
class DomainTable(models.Model):
    domain_id = models.CharField(
        primary_key=True, max_length=32, verbose_name="domain id"
    )
    domain_ip = models.GenericIPAddressField(verbose_name="domain ip")
    domain_port = models.IntegerField(verbose_name="domain port")
