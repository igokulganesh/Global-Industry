from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Salary)
admin.site.register(Employee)
admin.site.register(Products)
admin.site.register(Work)
admin.site.register(Orders)
admin.site.register(OrderItems)