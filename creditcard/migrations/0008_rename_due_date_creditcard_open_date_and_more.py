# Generated by Django 5.0.4 on 2024-06-06 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('creditcard', '0007_alter_creditcardapplication_creditcardexaminer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='creditcard',
            old_name='due_date',
            new_name='open_date',
        ),
        migrations.DeleteModel(
            name='SystemManager',
        ),
    ]
