from django import forms
from .models import PiggyBank, LineItem, Goal
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Row, Column, Div, HTML
from crispy_forms.bootstrap import InlineRadios
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
    Choices = (
        ('save', 'Save'),
        ('spend', 'Spend'),
    )
    save = forms.ChoiceField(choices=Choices, widget=forms.RadioSelect, label=False)

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
            Row(
                Column('item'), Column('date')),
            Row(
                Column(InlineRadios('save')),
                Column('amount'),
            ),

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
            'date': 'When do you hope to reach this goal?',
        }

    def __init__(self, user, *args, **kwargs):
        super(GoalForm, self).__init__(*args, **kwargs)
        self.fields['account'].initial = user.piggybank
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row('goalName'),
            Row(Column('amount'), Column('date')),
            Field('account', type='hidden'),
            Field('accomplished', type='hidden'),
            Submit('submit', 'Submit', css_class='btn btn-primary'),
        )


class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
