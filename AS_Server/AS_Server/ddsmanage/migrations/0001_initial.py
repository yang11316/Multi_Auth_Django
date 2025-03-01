# Generated by Django 4.0 on 2024-11-29 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DDSInfoTable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('entity_pid', models.CharField(max_length=32, verbose_name='entity pid')),
                ('dds_type', models.IntegerField(verbose_name='dds type')),
                ('protocol_type', models.IntegerField(verbose_name='protocol type')),
                ('source_ip', models.GenericIPAddressField(verbose_name='source ip')),
                ('source_port', models.IntegerField(verbose_name='source port')),
                ('source_mask', models.CharField(default='255.255.255.255', max_length=15, verbose_name='source mask')),
                ('source_mac', models.CharField(default='00:00:00:00:00:00', max_length=17, verbose_name='source mac')),
                ('destination_ip', models.GenericIPAddressField(verbose_name='destination ip')),
                ('destination_port', models.IntegerField(verbose_name='destination port')),
                ('destination_mask', models.CharField(default='255.255.255.255', max_length=15, verbose_name='destination mask')),
                ('destination_mac', models.CharField(default='00:00:00:00:00:00', max_length=17, verbose_name='destination mac')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='create time')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='update time')),
            ],
        ),
        migrations.CreateModel(
            name='PacketID',
            fields=[
                ('id', models.IntegerField(default=1, primary_key=True, serialize=False)),
                ('last_id', models.IntegerField(default=0)),
            ],
        ),
    ]
