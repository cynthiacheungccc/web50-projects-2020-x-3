# Generated by Django 2.0.3 on 2020-02-21 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_contact_indexshelf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indexshelf',
            name='image',
            field=models.FileField(upload_to='media'),
        ),
    ]
