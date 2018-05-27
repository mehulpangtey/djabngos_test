from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.UserProfile)
admin.site.register(models.Device_Detail_Feed)
admin.site.register(models.Corporate_Detail)
admin.site.register(models.Consumer_id)
admin.site.register(models.Consumer_pass)
