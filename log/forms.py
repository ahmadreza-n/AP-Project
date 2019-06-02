from django import forms

from .models import LogUser

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
# class BlogPostModelForm(forms.ModelForm):
#     class Meta:
#         model = BlogPost
#         fields = ['title', 'image', 'slug', 'content', 'publish_date']

#     def clean_title(self, *args, **kwargs):
#         instance = self.instance
#         title = self.cleaned_data.get('title')
#         qs = BlogPost.objects.filter(title__iexact=title)
#         if instance is not None:
#             qs = qs.exclude(pk=instance.pk) # id=instance.id
#         if qs.exists():
#             raise forms.ValidationError("This title has already been used. Please try again.")
#         return title
