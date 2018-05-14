# Generated by Django 2.0.4 on 2018-05-08 23:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0006_auto_20180427_0317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='album', to=settings.AUTH_USER_MODEL),
        ),
    ]