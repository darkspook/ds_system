# Generated by Django 3.0.7 on 2023-12-11 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery_inspection', '0009_delivery_deliverable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='deliverable',
            field=models.IntegerField(),
        ),
    ]
