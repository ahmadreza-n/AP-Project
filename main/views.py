from django.shortcuts import render, redirect


from .forms import (AccountModelForm, AccountForm,
                    GroupForm, ContactForm, AddMemberForm, ConsumerForm)
from .models import Account, Group, GroupMember


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
    groups = GroupMember.objects.filter(member=account)
    context = {"title": "Account Detail",
               'account': account, 'groups': groups}
    template_name = 'account.html'
    return render(request, template_name, context)


def sign_in_view(request):
    form = AccountForm(request.POST or None)
    if form.is_valid():
        try:
            account_id = form.data['account_id']
            password = form.data['password']
            accounts = Account.objects.filter(account_id=account_id,
                                              password=password)
            if len(accounts) == 1:
                return redirect(account_view, account_id=account_id)
            else:
                title = "Invalid data"
        except Exception as exeption:
            print(exeption)
    else:
        title = "Sign in"
    context = {'form': form, "title": title}
    template_name = 'sign-in.html'
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
    account = Account.objects.get(account_id=account_id)
    form = GroupForm(request.POST or None)
    if form.is_valid():
        try:
            group_id = form.data['group_id']
            group_name = form.data['group_name']
            group = Group(group_id=group_id, group_name=group_name, admin=account)
            group.save()
            GroupMember(group=group, member=account).save()
            return redirect(group_view, account_id=account_id, group_id=group_id)
        except Exception as exception:
            print(exception)
            title = "Add New Group Error"
    else:
        title = "Add New Group"
    template_name = 'add-group.html'
    context = {'form': form, 'title': title, 'account': account}
    return render(request, template_name, context)


def group_view(request, account_id, group_id):
    form = AddMemberForm(request.POST or None)
    if form.is_valid():
        try:
            member_id = form.data['member_id']
            group = Group.objects.get(group_id=group_id)
            member = Account.objects.get(account_id=member_id)
            group_member = GroupMember(group=group, member=member)
            group_member.save()
            return redirect(group_view,
                            account_id=account_id,
                            group_id=group_id)
        except Exception:
            title = 'Add New Member Error'
    else:
        title = 'Group'
    template_name = 'group.html'
    group = Group.objects.get(group_id=group_id)
    account = Account.objects.get(account_id=account_id)
    members = GroupMember.objects.filter(group_id=group_id)
    context = {'title': title, 'form': form,
                'group': group, 'members': members, 'account': account}
    return render(request, template_name, context)


def add_record_view(request, account_id, group_id):
    names_list = []
    if request.method == 'POST':
        for key, value in request.POST.lists():
            if key == 'sahm':
                names_list = value
        print(names_list)
    forms = [ConsumerForm(None), ConsumerForm(None)]
    template_name = 'add-record.html'
    # if forms[0].is_valid() and forms[1].is_valid():
    #     print('\n\n\n', forms[0].cleaned_data, '\n\n\n\n')
    #     print('\n\n\n', forms[1].cleaned_data, '\n\n\n\n')
    context = {'title': 'Add record', 'forms': forms}
    return render(request, template_name, context)