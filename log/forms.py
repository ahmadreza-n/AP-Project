from django import forms

from .models import LogUser, Group

# class BlogPostForm(forms.Form):
#     title = forms.CharField()
#     slug = forms.SlugField()
#     content = forms.CharField(widget=forms.Textarea)


class LogUserModelForm(forms.ModelForm):
    class Meta:
        model = LogUser
        fields = ['first_name', 'last_name',
                  'user_name', 'password', 'description']


class LogUserModelFormm(forms.ModelForm):
    class Meta:
        model = LogUser
        fields = ['user_name', 'password']


class GroupModelForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['group_name']
