from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class PinForm(forms.Form):
    title = forms.CharField(max_length=255, required=True)
    image = forms.ImageField(required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    tags = forms.CharField(max_length=255, required=False)

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        tags = [tag.strip() for tag in tags.split(',') if tag.strip()]
        return tags


class AddFavoritePinForm(forms.Form):
    pin_id = forms.IntegerField()
    user_id = forms.IntegerField()


class BoardForm(forms.Form):
    user_id = forms.IntegerField()
    title = forms.CharField(max_length=111, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
