from django import forms
from .models import Account, Group


class ContactForm(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea)

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        print(self.cleaned_data)
        print(email)
        if email.endswith(".edu"):
            raise forms.ValidationError(
                "This is not a valid email. Please don't use .edu.")
        return email


class AccountModelForm(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    class Meta:
        model = Account
        fields = ['first_name', 'last_name',
                  'account_id', 'password']


class AccountForm(forms.Form):
    account_id = forms.SlugField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)


class GroupForm(forms.Form):
    group_id = forms.SlugField(max_length=20)
    group_name = forms.CharField(max_length=20)


class AddMemberForm(forms.Form):
    member_id = forms.SlugField(max_length=20)
