# Generated by Django 4.0 on 2024-05-17 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('softwaremanage', '0003_alter_registersoftwarelocationtable_entity_ip_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='softwaretable',
            name='software_hash',
            field=models.CharField(max_length=32, verbose_name='software hash'),
        ),
    ]
