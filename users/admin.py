from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(AccountsCompany)
admin.site.register(AccountsFinancialdetail)
admin.site.register(AccountsOtherusersetting)
admin.site.register(AccountsUser)
# admin.site.register(AccountsSmscroutes)
# admin.site.register(AccountsSmppusers)

admin.site.register(ServicesSmpp)
admin.site.register(ServicesServicesSmpp)

# admin.site.register(WalletWallet)
# admin.site.register(WalletCampaignpassbook)
# admin.site.register(WalletPassbook)