# Generated by Django 3.1.13 on 2021-11-15 04:39

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0005_auto_20211115_1059'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='post',
            managers=[
                ('manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
