# Generated by Django 4.0.4 on 2022-05-14 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_rename_is_producer_account_role'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Account',
        ),
    ]
