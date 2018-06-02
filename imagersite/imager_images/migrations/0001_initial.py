# Generated by Django 2.0.6 on 2018-06-02 23:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):
    """
    Migration.
    """

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Untitled', max_length=180)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
                ('date_published', models.DateField(blank=True, null=True)),
                ('published', models.CharField(choices=[('PRIVATE', 'Private'), ('PUBLIC', 'Public')], max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', sorl.thumbnail.fields.ImageField(upload_to='images')),
                ('title', models.CharField(default='Untitled', max_length=250)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_uploaded', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
                ('date_published', models.DateField(blank=True, null=True)),
                ('published', models.CharField(choices=[('PRIVATE', 'Private'), ('PUBLIC', 'Public')], max_length=250)),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='photos',
            field=models.ManyToManyField(related_name='album', to='imager_images.Photo'),
        ),
        migrations.AddField(
            model_name='album',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='album', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='album',
            name='title',
            field=models.CharField(default='Untitled', max_length=250),
        ),
        migrations.AddField(
            model_name='album',
            name='cover',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='imager_images.Photo'),
        ),
        migrations.AddField(
            model_name='album',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
