from django import forms
from django.contrib.auth.models import User
from bank_system.models import Branch
from bank.models import Register


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    branch = forms.ModelChoiceField(
        queryset=Branch.objects.all(),
        empty_label="Select Branch"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class LoginForm(forms.Form):
    username=forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email'] 

class RegisterUpdateForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['profile_picture']




class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'city']  
       