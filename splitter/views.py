from django.shortcuts import render


from . import forms


def home_page(request):
    context = {"title": "Welcome to Splitter"}
    return render(request, "home.html", context)


def about_page(request):
    context = {"title": "About us"}
    return render(request, "about.html", context)


def contact_page(request):
    form = forms.ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        form = forms.ContactForm()
    context = {"title": "Contact us", "form": form}
    return render(request, "form.html", context)
