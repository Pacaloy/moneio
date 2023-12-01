from django.contrib import admin

from .models import User, Account, MoneyInOut, Transfer

# Register your models here.
admin.site.register(User)
admin.site.register(Account)
admin.site.register(MoneyInOut)
admin.site.register(Transfer)
