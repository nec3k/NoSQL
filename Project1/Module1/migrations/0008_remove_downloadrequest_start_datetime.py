# Generated by Django 4.2.5 on 2023-10-24 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Module1', '0007_remove_downloadrequest_finish_datetime_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='downloadrequest',
            name='start_datetime',
        ),
    ]
