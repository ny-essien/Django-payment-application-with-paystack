from django import forms
from .models import Payments


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payments
        fields = ['amount', 'email',]