from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','first_name','last_name','gender','role','MobileNo','password1','password2']
        widgets = {
            'gender':forms.Select(),
            'password1':forms.PasswordInput(),
            'password2':forms.PasswordInput(),
        }

class userlogin(forms.Form):
   email = forms.EmailField()
   password = forms.CharField(widget=forms.PasswordInput())
    
