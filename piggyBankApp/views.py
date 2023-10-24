from django.shortcuts import render, redirect
from .forms import PiggyBankForm, LineItemForm
from .models import PiggyBank, LineItem


# Create your views here.
def index(request):
    context = {'data': PiggyBank.objects.all()}
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


def addPiggyBank(request):
    if request.method == 'POST':
        form = PiggyBankForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.balance = instance.starting_balance
            form.save()
            return redirect(to='index')
    form = PiggyBankForm()
    context = {'form': form}
    return render(request, 'piggyBankApp/addPiggyBank.html', context)


def ledger(request):
    context = {
        'data': LineItem.objects.all().order_by('date'),
        'count': 0
    }
    return render(request, 'piggyBankApp/ledger.html', context)
