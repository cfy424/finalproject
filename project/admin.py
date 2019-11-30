from django.contrib import admin

from . import models

admin.site.register(models.Employee)
admin.site.register(models.EmployeeAddress)
admin.site.register(models.Customer)
admin.site.register(models.Case)
admin.site.register(models.CustomerAddress)
admin.site.register(models.OrderHistory)
admin.site.register(models.Product)
admin.site.register(models.Resolution)
# Register your models here.
