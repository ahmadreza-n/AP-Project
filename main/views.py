from django.shortcuts import render, redirect

from .func import (settle, update_group_balances,
                   update_group_balance_details, update_expense_balances)

from .forms import (UserForm,
                    GroupForm, ContactForm, AddMemberForm,
                    ExpenseForm, RatioForm, EditGroupModelForm)

from .forms import UserForm, ContactForm

from .models import (User, Account, Group, GroupMember, Expense,
                     ExpenseRatio, BalanceDetail)

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.utils import timezone


def home_view(request):
    username = request.user.__str__()
    if username == 'AnonymousUser':
        context = {'title': 'Welcome to Splitter'}
        return render(request, 'home.html', context)
    else:
        print('else')
        return redirect(account_view, username=username)


def about_view(request):
    context = {'title': 'About us'}
    return render(request, 'about.html', context)


def contact_view(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        form = ContactForm()
    context = {"title": "Contact us", "form": form}
    return render(request, "form.html", context)


def register_view(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        try:
            user = form.save()
            Account.objects.create(user=user)
            login(request, user)
            return redirect(account_view, username=user.get_username())
        except Exception as exception:
            print(exception)
    template_name = 'register.html'
    context = {'form': form, 'title': 'Register'}
    return render(request, template_name, context)


@login_required
def account_view(request, username):
    account = Account.objects.get(user=request.user)
    profile_account = Account.objects.get(
                user=User.objects.get(username=username))
    groups = GroupMember.objects.filter(member_fk=profile_account)
    if profile_account == account:
        template_name = 'account.html'
        title = 'Account Detail'
    else:
        template_name = 'profile.html'
        title = 'Profile Detail'
    context = {'title': title,
               'account': account, 'groups': groups,
               'profile_account': profile_account}
    return render(request, template_name, context)


def login_view(request):
    title = None
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = User.objects.get(username=username, password=password)
            # user = authenticate(request, username=username, password=password)
            # print('\n\n\n', username, password, '\n\n\n')
            # account = Account.objects.get(user=user)
            login(request, user)
            print(user)
            return redirect(account_view, username=user.get_username())
        except Exception as exeption:
            print(exeption)
    else:
        title = "Login"
    context = {"title": title}
    template_name = 'login.html'
    return render(request, template_name, context)


@login_required
def logout_view(request):
    if request.method == 'POST':
        if 'yes_sub' in request.POST:
            logout(request)
        elif 'no_sub' in request.POST:
            pass
        return redirect(home_view)
    template_name = 'logout.html'
    context = {'title': 'Logout'}
    return render(request, template_name, context)


@login_required
def add_group_view(request):
    account = Account.objects.get(user=request.user)
    if request.method == 'POST':
        try:
            group_id = request.POST['group_id']
            group_name = request.POST['group_name']
            group = Group.objects.create(group_id=group_id,
                                         group_name=group_name,
                                         admin_fk=account)
            GroupMember.objects.create(group_fk=group, member_fk=account)
            return redirect(group_view, group_id=group_id)
        except Exception as exception:
            print(exception)
            title = 'Add New Group Error'
    else:
        title = 'Add New Group'
    template_name = 'add-group.html'
    context = {'title': title, 'account': account}
    return render(request, template_name, context)

@login_required
def edit_group_view(request, group_id):
    account = Account.objects.get(user=request.user)
    group = Group.objects.get(group_id=group_id)
    form = EditGroupModelForm(request.POST or None, instance=group)
    if request.method == 'POST':
        try:
            group_name = form.data['group_name']
            group.group_name = group_name
            group.save()
            return redirect(group_view, group_id=group_id)
        except Exception as exception:
            print(exception)
            title = 'Edit Group Error'
    else:
        title = 'Edit Group'
    template_name = 'edit-group.html'
    print(group.group_name)
    context = {'form': form, 'title': title,
               'account': account, 'group': group}
    return render(request, template_name, context)


@login_required
def delete_group_view(request, group_id):
    group = Group.objects.get(group_id=group_id)
    if request.method == 'POST':
        if 'yes_sub' in request.POST:
            group.delete()
            return redirect(account_view, username=username)
        elif 'no_sub' in request.POST:
            return redirect(group_view, group_id=group_id)
    title = 'Delete Group'
    template_name = 'delete-group.html'
    context = {'title': title}
    return render(request, template_name, context)


@login_required
def settle_view(request, group_id, settler_id):
    account = Account.objects.get(user=request.user)
    group = Group.objects.get(group_id=group_id)
    settler = Account.objects.get(
                user=User.objects.get(username=settler_id))

    if request.method == 'POST':
        if 'yes_sub' in request.POST:
            settle(account, group, settler)
            return redirect(group_view, group_id=group_id)
        elif 'no_sub' in request.POST:
            return redirect(group_view, group_id=group_id)
    title = 'Settle Member'
    template_name = 'settle.html'
    context = {'title': title, 'settler': settler}
    return render(request, template_name, context)


@login_required
def group_view(request, group_id):
    if request.method == 'POST':
        try:
            member_id = request.POST['member_id']
            group = Group.objects.get(group_id=group_id)
            member = Account.objects.get(
                user=User.objects.get(username=member_id))
            GroupMember.objects.create(group_fk=group, member_fk=member)

            expenses = Expense.objects.filter(group_fk=group)
            for expense in expenses:
                ExpenseRatio.objects.create(expense_fk=expense, member_fk=member)
            return redirect(group_view, group_id=group_id)
        except Exception:
            title = 'Add New Member Error'
    else:
        title = 'Group'
    template_name = 'group.html'
    group = Group.objects.get(group_id=group_id)
    account = Account.objects.get(user=request.user)
    members = GroupMember.objects.filter(group_fk=group)
    expenses = Expense.objects.filter(group_fk=group)

    balance_details = BalanceDetail.objects.filter(group_fk=group)

    details = {}
    for member in members:
        temp = {}
        for balance_detail in balance_details:
            if balance_detail.debtor_fk == member.member_fk:
                temp[balance_detail.creditor_fk.user.username] = balance_detail.amount
            elif balance_detail.creditor_fk == member.member_fk:
                temp[balance_detail.debtor_fk.user.username] = balance_detail.amount
        details[member.member_fk.user.username] = temp

    context = {'title': title, 'group': group,
               'members': members, 'account': account,
               'expenses': expenses, 'details': details}
    return render(request, template_name, context)


@login_required
def add_expense_view(request, group_id):
    account = Account.objects.get(user=request.user)
    group = Group.objects.get(group_id=group_id)
    group_members = GroupMember.objects.filter(group_fk=group)
    form = ExpenseForm(request.POST or None)
    members = []
    ratio_forms = []
    for member in group_members:
        members.append(member.member_fk)
        ratio_form = RatioForm(None)
        ratio_form.label_suffix = member.member_fk.user.get_short_name()
        ratio_forms.append(ratio_form)
    if form.is_valid():
        try:
            for key, value in request.POST.lists():
                if key == 'ratio':
                    ratioes = value
            expense_type = 'payment'
            title = form.data['title']
            payer_id = form.data['payer_id']
            payer = Account.objects.get(
                user=User.objects.get(username=payer_id))
            cost = int(form.data['cost'])
            expense = Expense(expense_type=expense_type, group_fk=group, adder_fk=account,
                            payer_fk=payer, title=title, cost=cost)
            expense.save()
            for i in range(len(members)):
                ExpenseRatio.objects.create(expense_fk=expense,
                                           member_fk=members[i],
                                           ratio=ratioes[i])
            update_expense_balances(expense)
            update_group_balance_details(group)

            return redirect(group_view, group_id=group_id)
        except Exception as exception:
            print(exception)
            title = 'Add New Expense Error'
    else:
        title = 'Add New Expense'
    template_name = 'add-expense.html'
    context = {'form': form, 'ratio_forms': ratio_forms,
               'title': title, 'account': account}
    return render(request, template_name, context)


@login_required
def expense_view(request, group_id, expense_pk):
    # group = Group.objects.get(group_id=group_id)
    expense = Expense.objects.get(pk=expense_pk)
    ratioes = ExpenseRatio.objects.filter(expense_fk=expense)
    context = {'title': 'Account Detail',
               'expense': expense, 'ratioes': ratioes}
    template_name = 'expense.html'
    return render(request, template_name, context)
