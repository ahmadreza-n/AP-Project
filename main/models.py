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
    admin = models.ForeignKey(Account, to_field='account_id', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.group_id

    def get_absolute_url(self):
        return f"/{self.group_id}"


class GroupMember(models.Model):
    group = models.ForeignKey(Group, to_field='group_id', on_delete=models.CASCADE)
    member = models.ForeignKey(Account, to_field='account_id', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.member) + ' is in: ' + str(self.group)
