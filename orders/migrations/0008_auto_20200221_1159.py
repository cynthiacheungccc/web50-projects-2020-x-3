# Generated by Django 2.0.3 on 2020-02-21 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20200221_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indexshelf',
            name='image',
            field=models.FileField(upload_to='orders/static/media'),
        ),
    ]
