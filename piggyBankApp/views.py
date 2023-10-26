from django.shortcuts import render, redirect
from .forms import PiggyBankForm, LineItemForm, GoalForm, CustomUserForm
from .models import PiggyBank, LineItem, Goal, User
from django.contrib.auth import authenticate, login


# from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def index(request):
    bank = PiggyBank.objects.get(user_id=request.user.id)
    goal = Goal.objects.get(account_id=bank.id)
    progress = int((bank.balance / goal.amount) * 100)
    context = {'bank': bank,
               'goal': goal,
               'progress': progress }
    return render(request, 'piggyBankApp/index.html', context)


def addLineItem(request):
    if request.method == 'POST':
        form = LineItemForm(request.POST)
        if form.is_valid():
            instance = form.save()
            bank = PiggyBank.objects.get(id=instance.account_id)
            bank.balance += instance.amount
            bank.save()
            instance.save()
            return redirect(to='ledger')
    else:
        form = LineItemForm()

    context = {'form': form}
    return render(request, 'piggyBankApp/addLineItem.html', context)


def deleteLineItem(request, id):
    instance = LineItem.objects.get(id=id)
    bank = PiggyBank.objects.get(id=instance.account_id)
    bank.balance -= instance.amount
    bank.save()
    instance.delete()
    return redirect(to='ledger')


def addGoal(request):
    if request.method == 'POST':
        form = GoalForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='index')
    form = GoalForm(request.user)
    context = {'form': form}
    return render(request, 'piggyBankApp/addGoal.html', context)


def addPiggyBank(request):
    if request.method == 'POST':
        form = PiggyBankForm(request.user, request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.balance = instance.starting_balance
            form.save()
            return redirect(to='index')

    form = PiggyBankForm(request.user)
    context = {'form': form}
    return render(request, 'piggyBankApp/addPiggyBank.html', context)


def ledger(request):
    context = {
        'data': LineItem.objects.all().order_by('date'),
        'count': 0
    }
    return render(request, 'piggyBankApp/ledger.html', context)


def register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(to='addPiggyBank')
    else:
        form = CustomUserForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)
