# Generated by Django 3.1.2 on 2022-07-09 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20220707_1159'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='prod_name',
            new_name='product_name',
        ),
    ]