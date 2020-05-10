# Generated by Django 3.0.5 on 2020-05-06 10:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('picture', '0002_auto_20200426_1412'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='image',
        ),
        migrations.AddField(
            model_name='image',
            name='pic',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='images/%Y/%m/%d'),
            preserve_default=False,
        ),
    ]