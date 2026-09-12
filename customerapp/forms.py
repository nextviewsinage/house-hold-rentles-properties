from django  import forms
from customerapp import models
from django.contrib.auth.forms import PasswordChangeForm

class feedbackform(forms.ModelForm):
    class Meta:
        model = models.feedback
        fields = "__all__"
        

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