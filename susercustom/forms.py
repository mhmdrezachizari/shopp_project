from django import forms
from product.models import Discount
from accounts.models import User


class DiscountForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Select User")
    class Meta:
        model = Discount
        fields = ['user', 'discountCode' , 'valueDecimal']
