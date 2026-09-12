from django import forms
from .models import rentals, product, category, confirmorder
from django.contrib.auth.forms import PasswordChangeForm


class rentalsform(forms.ModelForm):
    class Meta:
        model = rentals
        fields = "__all__"
        exclude = ('user',)


class productform(forms.ModelForm):
    class Meta:
        model = product
        fields = "__all__"
        exclude = ('user',)


class categoryform(forms.ModelForm):
    class Meta:
        model = category
        fields = "__all__"
        exclude = ('user',)


class confirmorderform(forms.ModelForm):
    class Meta:
        model = confirmorder
        fields = "__all__"
        exclude = ('user',)


class PassForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Old Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


    
    
    
    
    
    
    
    
    
    
    