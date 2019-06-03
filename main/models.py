from django.db import models


class Account(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    account_id = models.SlugField(max_length=20, unique=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.account_id

    def get_absolute_url(self):
        return f"/add-group/{self.account_id}"


class Group(models.Model):
    group_id = models.SlugField(max_length=20, unique=True)
    group_name = models.CharField(max_length=20)
    # admin = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.group_id


class GroupAccount(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    # def __str__(self):
    #     return str(self.group.group_id) + ' ' + str(self.account.account_id)
