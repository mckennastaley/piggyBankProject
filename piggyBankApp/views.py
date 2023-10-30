from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import PiggyBankForm, LineItemForm, GoalForm, CustomUserForm
from .models import PiggyBank, LineItem, Goal, User
from django.contrib.auth import authenticate, login


# from django.contrib.auth.forms import UserCreationForm


# Create your views here.
@login_required
def index(request):
    lineItemForm = LineItemForm(request.user)
    bank = PiggyBank.objects.get(user_id=request.user.id)
    try:
        goal = Goal.objects.get(account_id=bank.id)
    except Goal.DoesNotExist:
        goal = None
    goalForm = GoalForm(request.user, instance=goal)

    if request.method == 'POST':
        if 'item' in request.POST:
            lineItemForm = LineItemForm(request.user, request.POST)
            if lineItemForm.is_valid():
                instance = lineItemForm.save()
                bank = PiggyBank.objects.get(id=instance.account_id)
                if lineItemForm['save'].data != 'save':
                    instance.amount *= -1
                bank.balance += instance.amount
                bank.save()
                instance.save()
        if 'goalName' in request.POST:
            goalForm = GoalForm(request.user, request.POST, instance=goal)
            if goalForm.is_valid():
                goal = goalForm.save()

    context = {'bank': bank,
               'goal': goal,
               'progress': 0,
               'lineItemForm': lineItemForm,
               'goalForm': goalForm,
               }

    if goal is not None:
        context['progress'] = int((bank.balance / goal.amount) * 100)
        return render(request, 'piggyBankApp/index.html', context)
    else:
        return render(request, 'piggyBankApp/index.html', context)


def addLineItem(request):
    if request.method == 'POST':
        form = LineItemForm(request.user, request.POST)
        if form.is_valid():
            instance = form.save()
            bank = PiggyBank.objects.get(id=instance.account_id)
            bank.balance += instance.amount
            bank.save()
            instance.save()
            return redirect(to='ledger')
    else:
        form = LineItemForm(request.user)

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
        'data': LineItem.objects.filter(account_id=request.user.piggybank.id).order_by('date'),
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
