# Generated by Django 4.1.5 on 2024-01-29 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_rename_address_line_2_address_address_line2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='address_line_1',
            new_name='address_line',
        ),
    ]
