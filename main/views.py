from django.shortcuts import render, redirect


from .forms import (AccountModelForm, AccountForm,
                    GroupForm, ContactForm)
from .models import Account, Group, GroupAccount


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


def sign_up_view(request):
    form = AccountModelForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(account_view, account_id=form.data['account_id'])
    template_name = 'sign-up.html'
    context = {'form': form, 'title': 'SignUp'}
    return render(request, template_name, context)


def account_view(request, account_id):
    account = Account.objects.get(account_id=account_id)
    context = {"title": "Account Detail",
               'account': account, 'groups': ['assef', 'ahmad']}
    template_name = 'account.html'
    return render(request, template_name, context)


def sign_in_view(request):
    form = AccountForm(request.POST or None)
    if form.is_valid():
        try:
            account_id = form.data['account_id']
            password = form.data['password']
            print(password)
            Account.objects.get(account_id=account_id, password=password)
            return redirect(account_view, account_id=account_id)
        except:
            template_name = 'sign-in.html'
            context = {'form': form, "title": "SignIn Error"}
            return render(request, template_name, context)
    template_name = 'sign-in.html'
    context = {'form': form, "title": "SignIn"}
    return render(request, template_name, context)


def sign_out_view(request):
    template_name = 'sign-out.html'
    context = {'title': 'Sign Out'}
    return render(request, template_name, context)


def list_view(request):
    accounts = Account.objects.all()
    template_name = 'list.html'
    context = {'accounts': accounts, 'title': 'List View'}
    return render(request, template_name, context)


def add_group_view(request, account_id):
    form = GroupForm(request.POST or None)
    if form.is_valid():
        try:
            group_id = form.data['group_id']
            group_name = form.data['group_name']
            account = Account.objects.get(account_id=account_id)
            group = Group(group_id=group_id, group_name=group_name)
            group.save()
            return redirect(group_view, account_id=account_id, group_id=group_id)
        except:
            template_name = 'add-group.html'
            context = {'form': form, "title": "Add New Group Error"}
            return render(request, template_name, context)
    else:
        template_name = 'add-group.html'
        account = Account.objects.get(account_id=account_id)
        context = {'form': form, "title": "Add New Group", 'account': account}
        return render(request, template_name, context)


def group_view(request, account_id, group_id):
    template_name = 'group.html'
    group = Group.objects.get(group_id=group_id)
    context = {'title': 'Group', 'group': group}
    return render(request, template_name, context)
