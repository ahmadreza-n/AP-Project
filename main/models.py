from django.db import models


class Account(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    account_id = models.SlugField(max_length=20, unique=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.account_id

    def get_add_url(self):
        return f"/add-group/{self.account_id}"

    def get_absolute_url(self):
        return f"/{self.account_id}"


class Group(models.Model):
    group_id = models.SlugField(max_length=20, unique=True)
    group_name = models.CharField(max_length=20)
    admin_id = models.ForeignKey(Account, to_field='account_id', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.group_id

    def get_absolute_url(self):
        return f"/{self.group_id}"


class GroupMember(models.Model):
    group_id = models.ForeignKey(Group, to_field='group_id', on_delete=models.CASCADE)
    member_id = models.ForeignKey(Account, to_field='account_id', on_delete=models.CASCADE)
    # group_id = models.CharField(max_length=20)
    # member_id = models.CharField(max_length=20)

    def __str__(self):
        return str(self.member_id) + ' is in: ' + str(self.group_id)
