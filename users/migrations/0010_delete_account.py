# Generated by Django 4.0.4 on 2022-05-14 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_account'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Account',
        ),
    ]
