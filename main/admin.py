from django.contrib import admin
from .models import (Account, Group, GroupMember,
                     Expense, ExpenseRatio, BalanceDetail)

admin.site.register(Account)
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(Expense)
admin.site.register(ExpenseRatio)
admin.site.register(BalanceDetail)
