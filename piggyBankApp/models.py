from django.db import models
import django.utils.timezone
from djmoney.models.fields import MoneyField

from datetime import date


# Create your models here.
class PiggyBank(models.Model):
    owner = models.CharField(max_length=20, null=False)
    starting_balance = MoneyField(null=False, max_digits=6,decimal_places=2, default_currency='USD', default=0)
    balance = MoneyField(null=True, blank=True, max_digits=6,decimal_places=2, default_currency='USD', default=0)

    def __str__(self):
        return f"{self.owner}'s Account"


class LineItem(models.Model):
    amount = MoneyField(null=False, max_digits=6, decimal_places=2, default_currency='USD')
    date = models.DateField(default=django.utils.timezone.now)
    item = models.CharField(max_length=100, null=False)
    account = models.ForeignKey(PiggyBank, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return f"Purchase of {self.item}"


