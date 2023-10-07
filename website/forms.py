from django import forms
from .models import Images,Feedback,AI_Response
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib.auth.models import User

# With this:
from website.models import User




class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username', 'required': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )


class UserCreation(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter your email'}))
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        labels = {"email": "Email"}

    def __init__(self, *args, **kwargs):
        super(UserCreation, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter your username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})



class ImagesForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image']


class DescriptionForm(forms.ModelForm):
    class Meta:
        model=AI_Response
        fields=['description']


class AI_ResponseForm(forms.ModelForm):
    class Meta:
        model=AI_Response
        fields=['image','value','result','description']