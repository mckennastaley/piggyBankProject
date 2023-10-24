from django import forms
from .models import PiggyBank, LineItem
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

class DateInput(forms.DateInput):
    input_type = 'date'


class PiggyBankForm(forms.ModelForm):
    class Meta:
        model = PiggyBank
        fields = '__all__'
        widgets = {
            'date': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super(PiggyBankForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('owner'),
            Field('starting_balance'),
            Submit('submit', 'Submit', css_class='btn btn-primary')
        )


class LineItemForm(forms.ModelForm):
    class Meta:
        model = LineItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LineItemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('amount'),
            Field('date'),
            Field('item'),
            Field('account'),
            Submit('submit', 'Submit', css_class='btn btn-primary'),
        )