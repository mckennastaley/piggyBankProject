from django.db import models
import django.utils.timezone
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import date


# Create your models here.
class PiggyBank(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    starting_balance = MoneyField(null=False, max_digits=6, decimal_places=2, default_currency='USD', default=0)
    balance = MoneyField(null=True, blank=True, max_digits=6, decimal_places=2, default_currency='USD', default=0)

    def __str__(self):
        return f"{self.user.first_name}'s Account"

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name}"


class Child(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bank = models.OneToOneField(PiggyBank, on_delete=models.CASCADE)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name}"


class LineItem(models.Model):
    amount = MoneyField(null=False, max_digits=6, decimal_places=2, default_currency='USD')
    date = models.DateField(default=django.utils.timezone.now)
    item = models.CharField(max_length=100, null=False)
    account = models.ForeignKey(PiggyBank, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return f"Purchase of {self.item}"


class Goal(models.Model):
    goalName = models.CharField(max_length=20, null=False)
    amount = MoneyField(max_digits=6, decimal_places=2, default_currency='USD')
    account = models.ForeignKey(PiggyBank, on_delete=models.CASCADE, blank=False)
    date = models.DateField()
    accomplished = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.goalName} for {self.account.owner}"
