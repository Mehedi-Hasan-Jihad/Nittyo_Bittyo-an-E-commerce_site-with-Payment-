# Generated by Django 3.1.2 on 2022-07-07 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20220707_1143'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='name',
            new_name='prod_name',
        ),
    ]
