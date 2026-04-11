from django import forms
from .models import Order

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['customer','dress_type','price','order_date','delivery_date','status']
