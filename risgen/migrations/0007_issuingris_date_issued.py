# Generated by Django 3.0.7 on 2023-12-26 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('risgen', '0006_remove_issuingris_supplier'),
    ]

    operations = [
        migrations.AddField(
            model_name='issuingris',
            name='date_issued',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]