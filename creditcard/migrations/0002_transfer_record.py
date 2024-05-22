# Generated by Django 5.0.6 on 2024-05-22 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creditcard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='transfer_record',
            fields=[
                ('transfer_record_id', models.AutoField(primary_key=True, serialize=False)),
                ('account_in_id', models.IntegerField()),
                ('account_out_id', models.IntegerField()),
                ('transfer_amount', models.IntegerField()),
                ('transfer_date', models.DateField()),
            ],
        ),
    ]
