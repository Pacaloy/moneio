# Generated by Django 4.2.3 on 2023-11-21 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moneio', '0012_alter_moneyinout_account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moneyinout',
            name='is_deductible',
        ),
    ]
