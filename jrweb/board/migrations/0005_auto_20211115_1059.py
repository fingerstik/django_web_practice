# Generated by Django 3.1.13 on 2021-11-15 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_auto_20211111_1037'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('body', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Posting',
        ),
    ]