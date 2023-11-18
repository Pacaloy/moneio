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
  is_floating = models.BooleanField()

  def __str__(self):
    return f"{self.user.username} -> isFloating:{self.is_floating} -> {self.name}: {self.initial_balance}"
  
  def serialize(self):
    return {
      "name": self.name,
      "balance": self.initial_balance,
      "date": self.initial_balance_date.strftime("%e %B %Y"),
      "is_floating": self.is_floating,
    }


class MoneyInOut(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="money_in_out_user")
  name = models.CharField(max_length=255)
  price = models.DecimalField(max_digits=12, decimal_places=2)
  date = models.DateField()
  is_deductible = models.BooleanField()
  account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="money_in_out_account")

  def __str__(self):
    return f"{self.user.username} -> isDeductible:{self.is_deductible} -> {self.account.name} -> {self.name}: {self.price}"
  
  def serialize(self):
    return {
      "name": self.name,
      "price": self.price,
      "date": self.date.strftime("%e %B %Y"),
      "account": self.account.name,
      "is_deductible": self.is_deductible,
    }
