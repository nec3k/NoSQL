# Generated by Django 4.2.5 on 2023-10-20 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Module1', '0003_alter_downloadrequest_finish_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='downloadformat',
            name='yt_dl_opts',
            field=models.JSONField(null=True),
        ),
    ]
