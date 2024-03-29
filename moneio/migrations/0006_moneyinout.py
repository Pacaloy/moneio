# Generated by Django 4.2.3 on 2023-11-16 16:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moneio', '0005_alter_account_user_delete_moneyinout'),
    ]

    operations = [
        migrations.CreateModel(
            name='MoneyInOut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('date', models.DateField()),
                ('is_expense', models.BooleanField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='money_in_out_account', to='moneio.account')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='money_in_out_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
