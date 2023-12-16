# Generated by Django 4.2.5 on 2023-12-16 12:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Module1', '0010_alter_downloadformat_file_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFormatPreference',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('format', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Module1.downloadformat', verbose_name='Preferovaný formát')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Uživatel')),
            ],
        ),
    ]
