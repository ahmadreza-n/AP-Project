from django.db import models


class Account(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    account_id = models.SlugField(max_length=20, unique=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.account_id

    def get_add_url(self):
        return f"/{self.account_id}/add-group"

    def get_absolute_url(self):
        return f"/{self.account_id}"


class Group(models.Model):
    group_id = models.SlugField(max_length=20, unique=True)
    group_name = models.CharField(max_length=20)
    admin_fk = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.group_id

    def get_absolute_url(self):
        return f"/{self.group_id}"


class Record(models.Model):
    group_fk = models.ForeignKey(Group, on_delete=models.CASCADE)
    account_fk = models.ForeignKey(Account, on_delete=models.CASCADE,
                                   related_name='account_fk_name')
    payer_fk = models.ForeignKey(Account, on_delete=models.CASCADE,
                                 related_name='payer_fk_name')
    title = models.CharField(max_length=20)
    cost = models.IntegerField()
    date_time = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/{self.title}"


class GroupMember(models.Model):
    group_fk = models.ForeignKey(Group, on_delete=models.CASCADE)
    member_fk = models.ForeignKey(Account, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.member_fk.account_id} is in {self.group_fk.group_name}'


class RecordRatio(models.Model):
    record_fk = models.ForeignKey(Record, on_delete=models.CASCADE)
    member_fk = models.ForeignKey(Account, on_delete=models.CASCADE)
    ratio = models.IntegerField(default=0)

    def __str__(self):
        s = f'"{self.member_fk.first_name}" used "{self.record_fk.title}"'
        s += f' by ratio of "{self.ratio}"'
        return s


class Pays(models.Model):
    group_fk = models.ForeignKey(Group, on_delete=models.CASCADE)
    member1_fk = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='member1')
    member2_fk = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='member2')
    mm_balance = models.IntegerField(default=0) # Member Member Balance

    def __str__(self):
        return self.group_fk.__str__()
