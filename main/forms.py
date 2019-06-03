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
    class Meta:
        model = Account
        fields = ['first_name', 'last_name',
                  'user_name', 'password', 'description']


class AccountModelFormm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['user_name', 'password']


class GroupModelForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['group_name']
