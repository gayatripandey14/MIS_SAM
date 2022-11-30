# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
import inspect


# class AccountsSmppusers(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     smpp_userdetails_id = models.IntegerField(unique=True)
#     date = models.DateTimeField()
#     on_submit = models.BooleanField(blank=True, null=True)
#     sale_price = models.FloatField()
#     route = models.ForeignKey('AccountsSmscroutes', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey('AccountsUser', models.DO_NOTHING)
#     assigned_to = models.ForeignKey('AccountsUser', models.DO_NOTHING, blank=True, null=True, related_name="client")

#     class Meta:
#         managed = False
#         db_table = 'accounts_smppusers'


# class AccountsSmscroutes(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     smpp_smsc_id = models.IntegerField(unique=True)
#     creation_type = models.CharField(max_length=100, blank=True, null=True)
#     company = models.CharField(max_length=100, blank=True, null=True)
#     operator = models.CharField(max_length=100, blank=True, null=True)
#     price = models.FloatField()
#     date = models.DateTimeField()
#     country = models.CharField(max_length=100, blank=True, null=True)
#     user = models.ForeignKey('AccountsUser', models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'accounts_smscroutes'

class AccountsCompany(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    company_address = models.CharField(max_length=200, blank=True, null=True)
    industry = models.CharField(max_length=300, blank=True, null=True)
    contact_person = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accounts_company'


class AccountsFinancialdetail(models.Model):
    id = models.AutoField(primary_key=True)
    currency = models.CharField(db_column='Currency', max_length=200, blank=True, null=True)  # Field name made lowercase.
    credit_limit = models.FloatField(blank=True, null=True)
    payment_terms = models.CharField(max_length=20, blank=True, null=True)
    change_on = models.CharField(max_length=50, blank=True, null=True)
    top_up = models.CharField(max_length=50, blank=True, null=True)
    bank_method = models.CharField(max_length=100, blank=True, null=True)
    notification = models.BooleanField()
    threshold_amount = models.FloatField(blank=True, null=True)
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    low_balance_email = models.CharField(max_length=200, blank=True, null=True)
    email_alert = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'accounts_financialdetail'


class AccountsOtherusersetting(models.Model):
    id = models.AutoField(primary_key=True)
    pricing_email = models.CharField(max_length=200, blank=True, null=True)
    finance_email = models.CharField(max_length=200, blank=True, null=True)
    support_email = models.CharField(max_length=200, blank=True, null=True)
    it_email = models.CharField(max_length=200, blank=True, null=True)
    status = models.BooleanField()
    agent_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accounts_otherusersetting'


class AccountsUser(models.Model):
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=datetime.now)
    email = models.CharField(unique=True, max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    user_type = models.CharField(max_length=20)
    address = models.CharField(max_length=200, blank=True, null=True)
    otp = models.IntegerField(blank=True, null=True)
    web_url = models.CharField(max_length=300, blank=True, null=True)
    support_no = models.CharField(max_length=200, blank=True, null=True)
    creation_type = models.CharField(max_length=20)
    creation_id = models.CharField(max_length=400, blank=True, null=True)
    otp_verified = models.BooleanField(default=True)
    company_detail = models.ForeignKey(AccountsCompany, models.DO_NOTHING, blank=True, null=True)
    created_by = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    financial_detail = models.ForeignKey(AccountsFinancialdetail, models.DO_NOTHING, blank=True, null=True)
    other_detail = models.ForeignKey(AccountsOtherusersetting, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accounts_user'





class AccountsUserlog(models.Model):
    id = models.AutoField(primary_key=True)
    action = models.CharField(max_length=20)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_userlog'




# """
class ServicesServicedetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_by = models.ForeignKey(AccountsUser, models.DO_NOTHING, blank=True, null=True)
    service_type = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    deduction_rate = models.FloatField()
    expiry_date = models.DateTimeField(blank=True, null=True)
    blocked = models.BooleanField(default=False)
    description = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(default=datetime.now())
    expired = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'services_servicedetail'
# """

class ServicesSmpp(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    tps = models.IntegerField(blank=True, null=True)
    private = models.BooleanField()
    service = models.ForeignKey(ServicesServicedetail, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'services_smpp'



class ServicesServices(models.Model):
    id = models.AutoField(primary_key=True)
    deduction_rate = models.FloatField()
    blocked = models.BooleanField(default=False)
    expiry_date = models.DateTimeField(blank=True, null=True)
    date = models.DateTimeField(default=datetime.now())
    expired = models.BooleanField(blank=True, null=True, default=False)
    added_by = models.ForeignKey(AccountsUser, models.DO_NOTHING, blank=True, null=True,related_name="Reseller")
    service = models.ForeignKey(ServicesServicedetail, models.DO_NOTHING)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)
    # smpp = models.ManyToManyField(ServicesSmpp,related_name="alloted_to",blank=True)

    class Meta:
        managed = False
        db_table = 'services_services'


class ServicesServicesSmpp(models.Model):
    id = models.AutoField(primary_key=True)
    services = models.ForeignKey(ServicesServices, models.DO_NOTHING)
    smpp = models.ForeignKey('ServicesSmpp', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'services_services_smpp'
        unique_together = (('services', 'smpp'),)


class WalletCampaignpassbook(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateTimeField()
    campaign_id = models.IntegerField(blank=True, null=True)
    campaign_name = models.CharField(max_length=100, blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)
    cost = models.FloatField()
    service = models.ForeignKey(ServicesServices, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wallet_campaignpassbook'


class WalletPassbook(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateTimeField(default=datetime.now())
    transanction_type = models.CharField(max_length=10)
    amount = models.FloatField()
    deduction_rate = models.FloatField()
    available_balance = models.FloatField(default=0.0)
    recieved_from = models.ForeignKey(AccountsUser, models.DO_NOTHING, blank=True, null=True,related_name="Recieved")
    sent_to = models.ForeignKey(AccountsUser, models.DO_NOTHING, blank=True, null=True,related_name="Sent")
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)
    wallet = models.ForeignKey('WalletWallet', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wallet_passbook'


class WalletWallet(models.Model):
    id = models.BigAutoField(primary_key=True)
    balance = models.FloatField(default=0.0)
    profit = models.FloatField(default=0.0)
    loss = models.FloatField(default=0.0)
    service = models.ForeignKey(ServicesServices, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wallet_wallet'





# creating wallet
@receiver(post_save, sender=ServicesServices)
def update_account_balance_on_order(instance, sender,created, **kwargs):
    
    if created:
        WalletWallet.objects.create(user=instance.user,service=instance)