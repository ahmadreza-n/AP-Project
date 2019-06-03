from django.shortcuts import render, redirect


from .forms import LogUserModelForm, LogUserModelFormm, GroupModelForm, ContactForm
from .models import LogUser, Group


def home_page(request):
    context = {"title": "Welcome to Splitter"}
    return render(request, "home.html", context)


def about_page(request):
    context = {"title": "About us"}
    return render(request, "about.html", context)


def contact_page(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        form = ContactForm()
    context = {"title": "Contact us", "form": form}
    return render(request, "form.html", context)


def user_detail_view(request, user_name):
    user = LogUser.objects.get(user_name=user_name)
    context = {"title": "User Detail",
               'user': user, 'groups': ['assef', 'ahmad']}
    template_name = 'user-detail.html'
    return render(request, template_name, context)


def sign_in_view(request):
    form = LogUserModelFormm(request.POST or None)
    if form.is_valid():
        try:
            user_name = form.data['user_name']
            password = form.data['password']
            user = LogUser.objects.get(user_name=user_name, password=password)
            return redirect(user_detail_view, user_name=user_name)
        except:
            template_name = 'sign-in.html'
            context = {'form': form, "title": "SignIn Error"}
            return render(request, template_name, context)
    template_name = 'sign-in.html'
    context = {'form': form, "title": "SignIn"}
    return render(request, template_name, context)


def sign_up_view(request):
    form = LogUserModelForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = LogUserModelForm()
    template_name = 'sign-up.html'
    context = {'form': form, 'title': 'SignUp'}
    return render(request, template_name, context)


def sign_out_view(request):
    template_name = 'sign-out.html'
    context = {'title': 'Sign Out'}
    return render(request, template_name, context)


def list_view(request):
    user_list = LogUser.objects.all()
    template_name = 'list.html'
    context = {'user_list': user_list, 'title': 'Logout'}
    return render(request, template_name, context)


def add_group_view(request, user_name):
    form = GroupModelForm(request.POST or None)
    if form.is_valid():
        try:
            print(form.data['group_name'])
            # group = Group.objects.create(group_name=form.group_name, admin=user_name)
        except:
            print('fuck')
    template_name = 'add-group.html'
    context = {'form': form, "title": "Add New Group"}
    return render(request, template_name, context)
