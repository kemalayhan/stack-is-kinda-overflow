from django import forms
from .models import User    

from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + \
            ('username', 'first_name', 'last_name', 'image', 'email', 'phone',
             'location', 'profession', 'experience', 'hourly_rate',
             'total_project', 'biography', 'github_link', 'tag', )



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'image', 'email', 'phone',
             'location', 'profession', 'experience', 'hourly_rate',
             'total_project', 'biography', 'github_link', 'tag',)