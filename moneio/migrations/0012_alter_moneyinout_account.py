# Generated by Django 4.2.3 on 2023-11-20 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moneio', '0011_alter_moneyinout_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneyinout',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='money_in_out_account', to='moneio.account'),
        ),
    ]