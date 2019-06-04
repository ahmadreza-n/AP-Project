from django.contrib import admin
from . import models

admin.site.register(models.Account)
admin.site.register(models.Group)
admin.site.register(models.GroupMember)
