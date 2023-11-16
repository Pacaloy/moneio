from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
  pass

  def __str__(self):
    return f"{self.id}: {self.username}"


class Account(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="account_user")
  name = models.CharField(max_length=255)
  initial_balance = models.DecimalField(max_digits=12, decimal_places=2)
  initial_balance_date = models.DateField()

  def __str__(self):
    return f"{self.user.username} -> {self.name}: {self.initial_balance}"


class MoneyInOut(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="money_in_out_user")
  name = models.CharField(max_length=255)
  price = models.DecimalField(max_digits=12, decimal_places=2)
  date = models.DateField()
  is_expense = models.BooleanField()
  account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="money_in_out_account")

  def __str__(self):
    return f"{self.user.username} -> {self.account.name} -> {self.name}: {self.price}"
