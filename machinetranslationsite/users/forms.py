from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField
    email = forms.EmailField

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField

    class Meta:
        model = Profile
        fields = ['image']


class TranslationFormEnglish(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 45}), initial='Hi, I am having a lovely day!')
    source_language = forms.CharField(initial='en', widget=forms.HiddenInput())
    target_language = forms.CharField(initial='tr', widget=forms.HiddenInput())


class TranslationFormTurkish(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 45}), initial="Merhaba, güzel bir gün geçiriyorum!")
    source_language = forms.CharField(initial='tr', widget=forms.HiddenInput())
    target_language = forms.CharField(initial='en', widget=forms.HiddenInput())
