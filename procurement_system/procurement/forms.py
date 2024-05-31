from django import forms
from .models import OrderItem, Contact


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'shop', 'quantity']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['type', 'value']