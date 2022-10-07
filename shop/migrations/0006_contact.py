# Generated by Django 3.1.2 on 2022-08-04 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20220709_1533'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('cid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=50)),
                ('phone', models.CharField(default='', max_length=50)),
                ('email', models.EmailField(default='', max_length=50)),
                ('desc', models.CharField(default='', max_length=50000)),
            ],
        ),
    ]