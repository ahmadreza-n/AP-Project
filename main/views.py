from django.shortcuts import render, redirect

from .func import (settle, update_group_balances,
                   update_group_balance_details, update_expense_balances)

from .forms import (UserForm, AccountForm,
                    GroupForm, ContactForm, AddMemberForm)

from .models import (User, Account, Group, GroupMember, Expense,
                     ExpenseRatio, BalanceDetail)

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


def home_view(request):
    user = request.user
    try:
        account = Account.objects.get(user=user)
        return redirect(account_view, username=account.user.get_username())
    except Exception as exception:
        print(exception)
        context = {'title': 'Welcome to Splitter'}
        return render(request, 'home.html', context)


def about_view(request):
    context = {'title': 'About us'}
    return render(request, 'about.html', context)


def contact_view(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form = ContactForm()
    context = {"title": "Contact us", "form": form}
    return render(request, "form.html", context)


def register_view(request):
    user_form = UserForm(request.POST or None)
    account_form = AccountForm(request.POST or None, request.FILES or None)
    if user_form.is_valid() and account_form.is_valid():
        try:
            user = user_form.save()
            account = account_form.save(commit=False)
            account.user = user
            if 'profile_picture' in request.FILES:
                account.profile_picture = request.FILES['profile_picture']
            account.save()
            login(request, user)
            return redirect(account_view, username=user.get_username())
        except Exception as exception:
            print(exception)
    template_name = 'register.html'
    context = {'title': 'Register', 'user_form': user_form,
               'account_form': account_form}
    return render(request, template_name, context)


@login_required(login_url='/login')
def account_view(request, username):
    account = Account.objects.get(user=request.user)
    profile_account = Account.objects.get(
        user=User.objects.get(username=username))
    groups = GroupMember.objects.filter(member_fk=profile_account)
    if profile_account == account:
        template_name = 'account.html'
        title = 'Account Detail'
        context = {'title': title,
                   'account': account, 'groups': groups}
        return render(request, template_name, context)
    else:
        return redirect(home_view)


def login_view(request):
    title = None
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = User.objects.get(username=username, password=password)
            login(request, user)
            return redirect(account_view, username=user.get_username())
        except Exception as exeption:
            print(exeption)
    else:
        title = "Login"
    context = {"title": title}
    template_name = 'login.html'
    return render(request, template_name, context)


@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect(home_view)


@login_required(login_url='/login')
def add_group_view(request):
    account = Account.objects.get(user=request.user)
    try:
        group_id = request.POST['group_id']
        group_name = request.POST['group_name']
        group = Group.objects.create(group_id=group_id,
                                     group_name=group_name,
                                     admin_fk=account)
        GroupMember.objects.create(group_fk=group, member_fk=account)
    except Exception as exception:
        print(exception)
        title = 'Add New Group Error'
    return redirect(group_view, group_id=group_id)


@login_required(login_url='/login')
def edit_group_view(request, group_id):
    account = Account.objects.get(user=request.user)
    group = Group.objects.get(group_id=group_id)
    try:
        group_name = request.POST['group_name']
        group.group_name = group_name
        group.save()
    except Exception as exception:
        print(exception)
        title = 'Edit Group Error'
    return redirect(group_view, group_id=group_id)


@login_required(login_url='/login')
def delete_group_view(request, group_id):
    group = Group.objects.get(group_id=group_id)
    group.delete()
    return redirect(account_view, username=request.user.get_username())


@login_required(login_url='/login')
def settle_view(request, group_id, settler_id):
    account = Account.objects.get(user=request.user)
    group = Group.objects.get(group_id=group_id)
    settler = Account.objects.get(
        user=User.objects.get(username=settler_id))

    settle(account, group, settler)
    return redirect(group_view, group_id=group_id)


@login_required(login_url='/login')
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
                ExpenseRatio.objects.create(
                    expense_fk=expense, member_fk=member)
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
    ratioes_list = []
    for expense in expenses:
        ratioes = ExpenseRatio.objects.filter(expense_fk=expense)
        ratioes_list.append(ratioes)
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
               'expenses': expenses, 'details': details,
               'ratioes_list': ratioes_list}
    return render(request, template_name, context)


@login_required(login_url='/login')
def add_expense_view(request, group_id):
    account = Account.objects.get(user=request.user)
    group = Group.objects.get(group_id=group_id)
    group_members = GroupMember.objects.filter(group_fk=group)
    members = []
    for member in group_members:
        members.append(member.member_fk)
    try:
        expense_type = 'payment'
        title = request.POST['title']
        payer_id = request.POST['payer_id']
        payer = Account.objects.get(
            user=User.objects.get(username=payer_id))
        cost = float(request.POST['cost'])
        expense = Expense(expense_type=expense_type, group_fk=group, adder_fk=account,
                          payer_fk=payer, title=title, cost=cost)
        expense.save()
        for member in members:
            ratio_of_username = f'ratio_of_{member.user.username}'
            ratio = float(request.POST[ratio_of_username])
            ExpenseRatio.objects.create(expense_fk=expense,
                                        member_fk=member,
                                        ratio=ratio)
        update_expense_balances(expense)
        update_group_balance_details(group)
    except Exception as exception:
        print(exception)
    return redirect(group_view, group_id=group_id)


@login_required(login_url='/login')
def delete_expense_view(request, group_id, expense_pk):
    expense = Expense.objects.get(pk=expense_pk)
    group = Group.objects.get(group_id=group_id)
    expense.delete()
    update_group_balances(group)
    update_group_balance_details(group)
    return redirect(group_view, group_id=group_id)


@login_required(login_url='/login')
def edit_expense_view(request, group_id, expense_pk):
    account = Account.objects.get(user=request.user)
    group = Group.objects.get(group_id=group_id)
    group_members = GroupMember.objects.filter(group_fk=group)
    expense = Expense.objects.get(pk=expense_pk)
    members = []
    for member in group_members:
        members.append(member.member_fk)
    try:
        expense.title = request.POST['title']
        payer_id = request.POST['payer_id']
        expense.payer_fk = Account.objects.get(
            user=User.objects.get(username=payer_id))

        expense.cost = float(request.POST['cost'])
        expense.save()
        for member in members:
            ratio_of_username = f'ratio_of_{member.user.username}'
            ratio = float(request.POST[ratio_of_username])
            expense_ratio = ExpenseRatio.objects.get(expense_fk=expense,
                                                     member_fk=member)
            expense_ratio.ratio = ratio
            expense_ratio.save()
        update_group_balances(group)
        update_group_balance_details(group)
    except Exception as exception:
        print(exception)
    return redirect(group_view, group_id=group_id)
