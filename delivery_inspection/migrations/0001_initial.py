# Generated by Django 3.0.7 on 2023-02-13 13:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iar_no', models.CharField(max_length=11, unique=True)),
                ('supplier', models.CharField(max_length=100)),
                ('purpose', models.TextField()),
                ('date_delivered', models.DateField()),
                ('image', models.ImageField(blank=True, upload_to='delivery_inspection/images/%Y/%m')),
                ('inspected_by', models.CharField(blank=True, max_length=100)),
                ('date_inspected', models.DateTimeField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('inspector', models.CharField(blank=True, max_length=100)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'deliveries',
            },
        ),
        migrations.CreateModel(
            name='PartialDelivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remarks', models.CharField(blank=True, max_length=200)),
                ('date_delivered', models.DateField()),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery_inspection.Delivery')),
                ('inspected_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'partial deliveries',
            },
        ),
    ]
