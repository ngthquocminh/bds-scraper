# Generated by Django 3.2.4 on 2021-06-10 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('WorkerID', models.AutoField(primary_key=True, serialize=False)),
                ('WorkerIP', models.CharField(max_length=15)),
                ('WorkerName', models.CharField(max_length=50)),
                ('RmqPassword', models.CharField(max_length=256)),
            ],
        ),
    ]