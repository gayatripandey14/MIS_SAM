from django.contrib import admin
from .models import AccountsSmppusers, AccountsSmscroutes


# Register your models here.
admin.site.register(AccountsSmppusers)
admin.site.register(AccountsSmscroutes)