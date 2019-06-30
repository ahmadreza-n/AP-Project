from . import models


def update_group_balances(group):
    group_members = models.GroupMember.objects.filter(group_fk=group)
    for group_member in group_members:
        group_member.balance = 0
        group_member.save()
    expenses = models.Expense.objects.filter(group_fk=group)
    for expense in expenses:
        update_expense_balances(expense)


def update_expense_balances(expense):
    group = expense.group_fk
    group_members = models.GroupMember.objects.filter(group_fk=group)
    expense_ratioes = models.ExpenseRatio.objects.filter(expense_fk=expense)
    cost = float(expense.cost)
    sum_of_ratioes = 0
    for expense_ratio in expense_ratioes:
        sum_of_ratioes += float(expense_ratio.ratio)
    member_payer = models.GroupMember.objects.get(group_fk=group,
                                                  member_fk=expense.payer_fk)
    member_payer.balance += cost
    member_payer.save()
    for group_member in group_members:
        ratio = float(expense_ratioes.get(
            member_fk=group_member.member_fk).ratio)
        group_member = models.GroupMember.objects.get(group_fk=group,
                                                      member_fk=group_member.member_fk)
        group_member.balance -= cost * ratio / sum_of_ratioes
        group_member.save()


def update_group_balance_details(group):
    group_members = models.GroupMember.objects.filter(group_fk=group)
    balances = {}
    for group_member in group_members:
        balances[group_member.member_fk.user.username] = group_member.balance
    balance_details = []
    epsilon = 0.0000001
    for i in range(len(group_members)):
        most_positive = max(balances, key=lambda k: balances[k])
        most_negative = min(balances, key=lambda k: balances[k])
        amount = 0
        if abs(balances[most_positive] - balances[most_negative]) < epsilon:
            break
        if abs(balances[most_positive]) < abs(balances[most_negative]):
            amount = abs(balances[most_positive])
            balances[most_negative] += amount
            balances[most_positive] = 0
        else:
            amount = abs(balances[most_negative])
            balances[most_positive] -= amount
            balances[most_negative] = 0
        balance_details.append((most_negative, amount, most_positive))

    temps = models.BalanceDetail.objects.filter(group_fk=group)
    for temp in temps:
        temp.delete()
    for balance_detail in balance_details:
        debtor_fk = models.Account.objects.get(
            user=models.User.objects.get(username=balance_detail[0]))
        creditor_fk = models.Account.objects.get(
            user=models.User.objects.get(username=balance_detail[2]))
        models.BalanceDetail.objects.create(group_fk=group, debtor_fk=debtor_fk,
                                            creditor_fk=creditor_fk, amount=balance_detail[1])


def settle(account, group, settler):
    members = models.GroupMember.objects.filter(group_fk=group)
    balance = models.GroupMember.objects.get(
        group_fk=group, member_fk=settler).balance
    if balance > 0:
        balance_details = models.BalanceDetail.objects.filter(
            group_fk=group, creditor_fk=settler)
    else:
        balance_details = models.BalanceDetail.objects.filter(
            group_fk=group, debtor_fk=settler)
    for balance_detail in balance_details:
        expense_type = 'settle'
        title = settler.user.username
        if balance > 0:
            title += ' took back from '
            title += balance_detail.debtor_fk.user.username
        else:
            title += ' paid back to '
            title += balance_detail.creditor_fk.user.username
        payer = balance_detail.debtor_fk
        cost = balance_detail.amount
        expense = models.Expense(expense_type=expense_type, group_fk=group,
                                 adder_fk=account, payer_fk=payer,
                                 title=title, cost=cost)
        expense.save()
        for i in range(len(members)):
            ratio = 0
            if members[i].member_fk == balance_detail.creditor_fk:
                ratio = 1
            models.ExpenseRatio.objects.create(expense_fk=expense,
                                               member_fk=members[i].member_fk,
                                               ratio=ratio)
        update_expense_balances(expense)
        update_group_balance_details(group)
