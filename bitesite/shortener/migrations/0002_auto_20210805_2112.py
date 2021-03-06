# Generated by Django 3.2.6 on 2021-08-05 16:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shortener', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='links',
            options={'ordering': ['-time_create', 'original_url'], 'verbose_name': 'Links', 'verbose_name_plural': 'Links'},
        ),
        migrations.AddField(
            model_name='links',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='links',
            name='original_url',
            field=models.URLField(max_length=255, verbose_name='Original url'),
        ),
        migrations.AlterField(
            model_name='links',
            name='shorten_url',
            field=models.CharField(blank=True, db_index=True, max_length=15, verbose_name='Short link'),
        ),
        migrations.AlterField(
            model_name='links',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time create'),
        ),
    ]
