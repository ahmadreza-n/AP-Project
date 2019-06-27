from . import models


def update_group_balances(group):
    group_members = models.GroupMember.objects.filter(group_fk=group)
    for group_member in group_members:
        group_member.balance = 0
        group_member.save()
    records = models.Record.objects.filter(group_fk=group)
    for record in records:
        update_record_balances(record)


def update_record_balances(record):
    group = record.group_fk
    group_members = models.GroupMember.objects.filter(group_fk=group)
    record_ratioes = models.RecordRatio.objects.filter(record_fk=record)
    cost = int(record.cost)
    sum_of_ratioes = 0
    for record_ratio in record_ratioes:
        sum_of_ratioes += int(record_ratio.ratio)
    member_payer = models.GroupMember.objects.get(group_fk=group,
                                                  member_fk=record.payer_fk)
    member_payer.balance += cost
    member_payer.save()
    # group_members = models.GroupMember.objects.filter(group_fk=group)
    for group_member in group_members:
        ratio = int(record_ratioes.get(member_fk=group_member.member_fk).ratio)
        group_member = models.GroupMember.objects.get(group_fk=group,
                                                      member_fk=group_member.member_fk)
        group_member.balance -= cost * ratio / sum_of_ratioes
        print(group_member.balance)
        group_member.save()


def update_record_mm_balances(record):
    group = record.group_fk
    group_members = models.GroupMember.objects.filter(group_fk=group)
    balances = {}
    for group_member in group_members:
        balances[group_member.member_fk.account_id] = group_member.balance
    print(balances)
    # balances = {'assef': +12, 'mamraz': +21, 'sajjad': -20, 'saleh': -5, 'unes': -8}
    pays = []
    while True:
        most_positive = max(balances, key=lambda k: balances[k])
        most_negative = min(balances, key=lambda k: balances[k])
        pay_amount = 0
        if balances[most_positive] == balances[most_negative]:
            break
        if abs(balances[most_positive]) < abs(balances[most_negative]):
            pay_amount = abs(balances[most_positive])
            balances[most_negative] += pay_amount
            balances[most_positive] = 0
        else:
            pay_amount = abs(balances[most_negative])
            balances[most_positive] -= pay_amount
            balances[most_negative] = 0
        pays.append((most_negative, pay_amount, most_positive))

    temps = models.Pays.objects.filter(group_fk=group)
    for temp in temps:
        temp.delete()
    for pay in pays:
        member1_fk = models.Account.objects.get(account_id=pay[0])
        member2_fk = models.Account.objects.get(account_id=pay[2])
        models.Pays.objects.create(group_fk=group, member1_fk=member1_fk,
                                   member2_fk=member2_fk, mm_balance=pay[1])
