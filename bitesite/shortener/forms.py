from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Links, Feedback


class ShortenLinkForm(forms.ModelForm):
    original_url = forms.CharField(label='Original URL', widget=forms.TextInput(attrs={'class': 'home-shortener_url',
                                                                                       'placeholder': 'https://example.org/3/library/example/2/example.html'}))

    class Meta:
        model = Links
        fields = ['original_url']


class UserShortenLinkForm(forms.ModelForm):
    original_url = forms.CharField(label='Original URL', widget=forms.TextInput(attrs={'class': 'home-shortener_url',
                                                                                       'placeholder': 'https://example.org/3/library/example/2/example.html'}))
    shorten_url = forms.CharField(label='Shorten URL', widget=forms.TextInput(attrs={'class': 'home-shortener_url',
                                                                                     'placeholder': 'short name'}))

    class Meta:
        model = Links
        fields = ['original_url', 'shorten_url']


class FeedbackForm(forms.ModelForm):
    sender = forms.EmailField(label='Sender', widget=forms.TextInput(attrs={'placeholder': 'user@localhost.com'}))
    message = forms.CharField(label='Message', widget=forms.Textarea(attrs={'placeholder': 'Leave your message here...'}))

    class Meta:
        model = Feedback
        fields = ['sender', 'message']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login:', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email:', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password:', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Repeat password:', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login:', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password:', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
