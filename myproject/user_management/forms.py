from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.USER_ROLES)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'role')
