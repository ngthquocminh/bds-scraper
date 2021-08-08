# Generated by Django 3.2.4 on 2021-06-12 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Workers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('site', models.CharField(max_length=64)),
                ('features', models.CharField(max_length=32)),
                ('default', models.CharField(max_length=256)),
                ('xpath', models.CharField(max_length=256)),
                ('pos_take', models.CharField(max_length=256)),
                ('regex_take', models.CharField(max_length=256)),
                ('regex_valid', models.CharField(max_length=256)),
                ('len_valid', models.IntegerField()),
            ],
        ),
    ]