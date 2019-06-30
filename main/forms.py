from django import forms
from .models import User, Group, Account


class ContactForm(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea)


class UserForm(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'password']


class AccountForm(forms.ModelForm):
    class Meta():
        model = Account
        fields = ['profile_picture']


class GroupForm(forms.Form):
    group_id = forms.SlugField(max_length=20)
    group_name = forms.CharField(max_length=20)


class AddMemberForm(forms.Form):
    member_id = forms.SlugField(max_length=20)
