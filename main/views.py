from django.shortcuts import render, redirect

from . import func
from .forms import (AccountModelForm, AccountForm,
                    GroupForm, ContactForm, AddMemberForm,
                    RecordForm, RatioForm)
from .models import Account, Group, GroupMember, Record, RecordRatio
# from django.utils import timezone


def home_page(request):
    context = {'title': 'Welcome to Splitter'}
    # group = Group.objects.get(group_id='dorm')
    # func.update_group_balances(group)
    return render(request, 'home.html', context)


def about_page(request):
    context = {'title': 'About us'}
    return render(request, 'about.html', context)


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
    groups = GroupMember.objects.filter(member_fk=account)
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
            group = Group(group_id=group_id, group_name=group_name,
                          admin_fk=account)
            group.save()
            GroupMember(group_fk=group, member_fk=account).save()
            return redirect(group_view, account_id=account_id,
                            group_id=group_id)
        except Exception as exception:
            print(exception)
            title = 'Add New Group Error'
    else:
        title = 'Add New Group'
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
            group_member = GroupMember(group_fk=group, member_fk=member)
            group_member.save()
            records = Record.objects.filter(group_fk=group)
            for record in records:
                RecordRatio.objects.create(record_fk=record, member_fk=member,)
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
    members = GroupMember.objects.filter(group_fk=group)
    records = Record.objects.filter(group_fk=group)
    context = {'title': title, 'form': form,
               'group': group, 'members': members, 'account': account,
               'records': records}
    return render(request, template_name, context)


def add_record_view(request, account_id, group_id):
    account = Account.objects.get(account_id=account_id)
    group = Group.objects.get(group_id=group_id)
    group_members = GroupMember.objects.filter(group_fk=group)
    form = RecordForm(request.POST or None)
    members = []
    ratio_forms = []
    for member in group_members:
        members.append(member.member_fk)
        ratio_form = RatioForm(None)
        ratio_form.label_suffix = member.member_fk.first_name
        ratio_forms.append(ratio_form)
    if form.is_valid():
        try:
            for key, value in request.POST.lists():
                if key == 'ratio':
                    ratioes = value
            title = form.data['title']
            payer_id = form.data['payer_id']
            payer = Account.objects.get(account_id=payer_id)
            cost = int(form.data['cost'])
            record = Record(group_fk=group, account_fk=account,
                            payer_fk=payer, title=title, cost=cost)
            record.save()
            for i in range(len(members)):
                RecordRatio.objects.create(record_fk=record,
                                            member_fk=members[i],
                                            ratio=ratioes[i])
            func.update_record_balances(record)

            return redirect(group_view, account_id=account_id,
                            group_id=group_id)
        except Exception as exception:
            print(exception)
            title = 'Add New Record Error'
    else:
        title = 'Add New Record'
    template_name = 'add-record.html'
    context = {'form': form, 'ratio_forms': ratio_forms,
               'title': title, 'account': account}
    return render(request, template_name, context)


def record_view(request, account_id, group_id, record_pk):
    # account = Account.objects.get(account_id=account_id)
    # group = Group.objects.get(group_id=group_id)
    record = Record.objects.get(pk=record_pk)
    ratioes = RecordRatio.objects.filter(record_fk=record)
    context = {'title': 'Account Detail',
               'record': record, 'ratioes': ratioes}
    template_name = 'record.html'
    return render(request, template_name, context)
