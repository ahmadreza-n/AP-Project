from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # first_name = models.CharField(max_length=20)
    # last_name = models.CharField(max_length=20)
    # account_id = models.SlugField(max_length=20, unique=True)
    # password = models.CharField(max_length=20)
    profile_picture = models.ImageField(
        upload_to='main/static/img/profile_pictures', blank=True)

    def __str__(self):
        return self.user.get_username()

    def get_add_url(self):
        return f"/add-group"

    def get_absolute_url(self):
        return f"{self.user.get_username()}"

    def get_profile_picture_address(self):
        return self.profile_picture.url[4:]


class Group(models.Model):
    group_id = models.SlugField(max_length=20, unique=True)
    group_name = models.CharField(max_length=20)
    admin_fk = models.ForeignKey(Account, on_delete=models.CASCADE)
    group_picture = models.ImageField(
        upload_to='main/static/img/group_pictures', blank=True)

    def __str__(self):
        return self.group_id

    def get_absolute_url(self):
        return f"/{self.group_id}"

    def get_group_picture_address(self):
        return self.group_picture.url[4:]


class Expense(models.Model):
    expense_type = models.CharField(max_length=10, default='payment')
    group_fk = models.ForeignKey(Group, on_delete=models.CASCADE)
    adder_fk = models.ForeignKey(Account, on_delete=models.CASCADE,
                                 related_name='adder_fk')
    payer_fk = models.ForeignKey(Account, on_delete=models.CASCADE,
                                 related_name='payer_fk')
    title = models.CharField(max_length=20)
    cost = models.FloatField(default=0)
    date_time = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return f"/{self.title}"


class GroupMember(models.Model):
    group_fk = models.ForeignKey(Group, on_delete=models.CASCADE)
    member_fk = models.ForeignKey(Account, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)

    def __str__(self):
        return f'{self.member_fk.user.get_username()} is in {self.group_fk.group_name}'


class ExpenseRatio(models.Model):
    expense_fk = models.ForeignKey(Expense, on_delete=models.CASCADE)
    member_fk = models.ForeignKey(Account, on_delete=models.CASCADE)
    ratio = models.FloatField(default=0)

    def __str__(self):
        s = f'"{self.member_fk.user.username}" used "{self.expense_fk.title}"'
        s += f' by ratio of "{self.ratio}"'
        return s


class BalanceDetail(models.Model):
    group_fk = models.ForeignKey(Group, on_delete=models.CASCADE)
    debtor_fk = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='debtor')  # related name #########
    creditor_fk = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='creditor')
    amount = models.FloatField(default=0)

    def __str__(self):
        string = f'{self.debtor_fk.user.username} '
        string += f'owes {self.amount} '
        string += f'to {self.creditor_fk.user.username} '
        string += f'in {self.group_fk.group_id}'
        return string
