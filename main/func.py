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
