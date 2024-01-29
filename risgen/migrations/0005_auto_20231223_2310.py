# Generated by Django 3.0.7 on 2023-12-23 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('risgen', '0004_completeddia_with_ris_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issuingris',
            name='item_description',
        ),
        migrations.RemoveField(
            model_name='issuingris',
            name='qty',
        ),
        migrations.RemoveField(
            model_name='issuingris',
            name='remarks',
        ),
        migrations.RemoveField(
            model_name='issuingris',
            name='stock_no',
        ),
        migrations.RemoveField(
            model_name='issuingris',
            name='unit',
        ),
        migrations.CreateModel(
            name='IssuingRISItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_no', models.IntegerField(null=True)),
                ('unit', models.CharField(max_length=100)),
                ('item_description', models.TextField()),
                ('qty', models.CharField(max_length=7)),
                ('remarks', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('ris_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='risgen.IssuingRIS')),
            ],
            options={
                'verbose_name_plural': 'Issuing RIS Items',
            },
        ),
    ]