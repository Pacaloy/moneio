# Generated by Django 4.2.3 on 2023-11-17 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moneio', '0007_account_is_floating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='moneyinout',
            old_name='is_expense',
            new_name='is_deductibles',
        ),
    ]