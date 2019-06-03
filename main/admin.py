from django.contrib import admin
from . import models

admin.site.register(models.LogUser)
admin.site.register(models.Group)
