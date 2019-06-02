from django.shortcuts import render


from .forms import ContactForm
from blog.models import BlogPost


def home_page(request):
    qs = BlogPost.objects.all()[:5]
    context = {"title": "Welcome to Splitter", 'blog_list': qs}
    return render(request, "home.html", context)


def about_page(request):
    context = {"title": "About us"}
    return render(request, "about.html", context)


def contact_page(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        form = ContactForm()
    context = {
        "title": "Contact us",
        "form": form
    }
    return render(request, "form.html", context)
