# Generated by Django 3.0.7 on 2022-05-17 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ict_inventory', '0005_auto_20220517_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='asset',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ict_inventory.Asset'),
        ),
    ]
