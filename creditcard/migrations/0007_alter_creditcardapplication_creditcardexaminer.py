# Generated by Django 5.0.4 on 2024-05-31 07:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creditcard', '0006_alter_creditcard_online_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcardapplication',
            name='creditCardExaminer',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='creditcard.creditcardexaminer'),
        ),
    ]