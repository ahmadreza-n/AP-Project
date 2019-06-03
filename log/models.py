# from django.conf import settings
from django.db import models
# from django.db.models import Q
# from django.utils import timezone


class LogUser(models.Model):  # blogpost_set -> queryset
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    user_name = models.SlugField(max_length=20)
    password = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user_name

    def get_absolute_url(self):
        return f"/log/add-group/{self.user_name}"


class Group(models.Model):
    group_name = models.CharField(max_length=20)
    admin = models.ForeignKey(LogUser, on_delete=models.CASCADE)


class GroupUser(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(LogUser, on_delete=models.CASCADE)
