# Generated by Django 3.0.7 on 2023-02-20 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ictinv', '0003_auto_20230130_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]