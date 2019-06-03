from django.db import models


class Account(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    user_name = models.SlugField(max_length=20)
    password = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user_name

    def get_absolute_url(self):
        return f"/add-group/{self.user_name}"


class Group(models.Model):
    group_name = models.CharField(max_length=20)
    admin = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.group_name


class GroupUser(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
