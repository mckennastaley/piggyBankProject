from django import forms
from .models import PiggyBank, LineItem, Goal
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.core.exceptions import ValidationError


class DateInput(forms.DateInput):
    input_type = 'date'


class PiggyBankForm(forms.ModelForm):
    class Meta:
        model = PiggyBank
        fields = '__all__'

    def __init__(self, user, *args, **kwargs):
        super(PiggyBankForm, self).__init__(*args, **kwargs)
        self.fields['user'].initial = user
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('user', type='hidden'),
            Field('starting_balance'),
            Submit('submit', 'Submit', css_class='btn btn-primary')
        )


class LineItemForm(forms.ModelForm):
    class Meta:
        model = LineItem
        fields = '__all__'
        widgets = {
            'date': DateInput(),
        }

    def __init__(self, user, *args, **kwargs):
        super(LineItemForm, self).__init__(*args, **kwargs)
        self.fields['account'].initial = user.piggybank
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('item'),
            Field('amount'),
            Field('date'),
            Field('account', type='hidden'),
            Submit('submit', 'Submit', css_class='btn btn-primary'),
        )


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = '__all__'
        widgets = {
            'date': DateInput()
        }
        labels = {
            'item': 'What are you saving for?',
            'amount': 'How much does it cost?',
            'date': 'What day do you hope to reach this goal?',
        }

    def __init__(self, user, *args, **kwargs):
        super(GoalForm, self).__init__(*args, **kwargs)
        self.fields['account'].initial = user.piggybank
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('goalName'),
            Field('amount'),
            Field('date'),
            Field('account', type='hidden'),
            Field('accomplished', type='hidden'),
            Submit('submit', 'Submit', css_class='btn btn-primary'),
        )


class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
