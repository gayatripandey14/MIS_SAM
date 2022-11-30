# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AltSendSms(models.Model):
    sql_id = models.BigAutoField(primary_key=True)
    momt = models.CharField(max_length=3, blank=True, null=True)
    sender = models.CharField(max_length=20, blank=True, null=True)
    receiver = models.CharField(max_length=20, blank=True, null=True)
    udhdata = models.TextField(blank=True, null=True)
    msgdata = models.TextField(blank=True, null=True)
    time = models.BigIntegerField(blank=True, null=True)
    smsc_id = models.CharField(max_length=255, blank=True, null=True)
    service = models.CharField(max_length=255, blank=True, null=True)
    account = models.CharField(max_length=255, blank=True, null=True)
    id = models.BigIntegerField(blank=True, null=True)
    sms_type = models.BigIntegerField(blank=True, null=True)
    mclass = models.BigIntegerField(blank=True, null=True)
    mwi = models.BigIntegerField(blank=True, null=True)
    coding = models.BigIntegerField(blank=True, null=True)
    compress = models.BigIntegerField(blank=True, null=True)
    validity = models.BigIntegerField(blank=True, null=True)
    deferred = models.BigIntegerField(blank=True, null=True)
    dlr_mask = models.BigIntegerField(blank=True, null=True)
    dlr_url = models.CharField(max_length=255, blank=True, null=True)
    pid = models.BigIntegerField(blank=True, null=True)
    alt_dcs = models.BigIntegerField(blank=True, null=True)
    rpi = models.BigIntegerField(blank=True, null=True)
    charset = models.CharField(max_length=255, blank=True, null=True)
    boxc_id = models.CharField(max_length=255, blank=True, null=True)
    binfo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alt_send_sms'


class DeliverSm(models.Model):
    smpp_id = models.BigAutoField(primary_key=True)
    type = models.IntegerField(blank=True, null=True)
    sender = models.CharField(max_length=20, blank=True, null=True)
    receiver = models.CharField(max_length=20, blank=True, null=True)
    msgdata = models.TextField(blank=True, null=True)
    messageid = models.CharField(max_length=50, blank=True, null=True)
    routeid = models.CharField(max_length=20, blank=True, null=True)
    boxid = models.CharField(max_length=15, blank=True, null=True)
    userid = models.CharField(max_length=15, blank=True, null=True)
    error_code = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'deliver_sm'


class DlrCeletelairtel(models.Model):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.CharField(max_length=40)
    source = models.CharField(max_length=25, blank=True, null=True)
    destination = models.CharField(max_length=25)
    url = models.TextField(blank=True, null=True)
    mask = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    boxcid = models.CharField(max_length=25, blank=True, null=True)
    datetime = models.DateTimeField()
    msg_parts = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dlr_celetelairtel'


class DlrDemo(models.Model):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.CharField(max_length=40)
    source = models.CharField(max_length=25, blank=True, null=True)
    destination = models.CharField(max_length=25)
    url = models.TextField(blank=True, null=True)
    mask = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    boxcid = models.CharField(max_length=25, blank=True, null=True)
    datetime = models.DateTimeField()
    msg_parts = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dlr_demo'


class DlrTestnewsmpp(models.Model):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.CharField(max_length=40)
    source = models.CharField(max_length=25, blank=True, null=True)
    destination = models.CharField(max_length=25)
    url = models.TextField(blank=True, null=True)
    mask = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    boxcid = models.CharField(max_length=25, blank=True, null=True)
    datetime = models.DateTimeField()
    msg_parts = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dlr_testnewsmpp'


class LongMessageParts(models.Model):
    userid = models.CharField(max_length=30)
    senderid = models.CharField(max_length=16)
    tonumber = models.CharField(max_length=16)
    udh = models.CharField(max_length=30)
    message_parts = models.IntegerField()
    part_number = models.IntegerField()
    message_text = models.CharField(max_length=500, blank=True, null=True)
    create_date = models.DateTimeField()
    message_id = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'long_message_parts'
        unique_together = (('senderid', 'userid', 'tonumber', 'udh', 'part_number', 'message_parts'),)


class SendSms(models.Model):
    sql_id = models.BigAutoField(primary_key=True)
    momt = models.CharField(max_length=2, blank=True, null=True)
    sender = models.CharField(max_length=20, blank=True, null=True)
    receiver = models.CharField(max_length=20, blank=True, null=True)
    udhdata = models.TextField(blank=True, null=True)
    msgdata = models.TextField(blank=True, null=True)
    time = models.BigIntegerField(blank=True, null=True)
    smsc_id = models.CharField(max_length=255, blank=True, null=True)
    service = models.CharField(max_length=255, blank=True, null=True)
    account = models.CharField(max_length=255, blank=True, null=True)
    id = models.BigIntegerField(blank=True, null=True)
    sms_type = models.BigIntegerField(blank=True, null=True)
    mclass = models.BigIntegerField(blank=True, null=True)
    mwi = models.BigIntegerField(blank=True, null=True)
    coding = models.BigIntegerField(blank=True, null=True)
    compress = models.BigIntegerField(blank=True, null=True)
    validity = models.BigIntegerField(blank=True, null=True)
    deferred = models.BigIntegerField(blank=True, null=True)
    dlr_mask = models.BigIntegerField(blank=True, null=True)
    dlr_url = models.CharField(max_length=255, blank=True, null=True)
    pid = models.BigIntegerField(blank=True, null=True)
    alt_dcs = models.BigIntegerField(blank=True, null=True)
    rpi = models.BigIntegerField(blank=True, null=True)
    charset = models.CharField(max_length=255, blank=True, null=True)
    boxc_id = models.CharField(max_length=255, blank=True, null=True)
    binfo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'send_sms'


class SmppRoute(models.Model):
    id = models.BigAutoField(primary_key=True)
    system_id = models.CharField(max_length=100)
    smsc_id = models.CharField(max_length=100)
    percentage = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'smpp_route'
        unique_together = (('system_id', 'smsc_id'),)


class SmppSmsc(models.Model):
    smsc_id = models.CharField(db_column='smsc-id', max_length=20,unique=True)  # Field renamed to remove unsuitable characters.
    alt_charset = models.CharField(db_column='alt-charset', max_length=20)  # Field renamed to remove unsuitable characters.
    transceiver_mode = models.CharField(db_column='transceiver-mode', max_length=20)  # Field renamed to remove unsuitable characters.
    host = models.CharField(max_length=20)
    port = models.IntegerField()
    smsc_username = models.CharField(db_column='smsc-username', max_length=20)  # Field renamed to remove unsuitable characters.
    smsc_password = models.CharField(db_column='smsc-password', max_length=20)  # Field renamed to remove unsuitable characters.
    system_type = models.CharField(db_column='system-type', max_length=20)  # Field renamed to remove unsuitable characters.
    source_addr_ton = models.IntegerField(db_column='source-addr-ton')  # Field renamed to remove unsuitable characters.
    source_addr_npi = models.IntegerField(db_column='source-addr-npi')  # Field renamed to remove unsuitable characters.
    dest_addr_ton = models.IntegerField(db_column='dest-addr-ton')  # Field renamed to remove unsuitable characters.
    dest_addr_npi = models.IntegerField(db_column='dest-addr-npi')  # Field renamed to remove unsuitable characters.
    throughput = models.IntegerField()
    instances = models.IntegerField()
    # conn_type = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'smpp_smsc'

class SmppUser(models.Model):
    system_id = models.CharField(primary_key=True, max_length=15)
    password = models.CharField(max_length=64)
    throughput = models.FloatField()
    default_smsc = models.CharField(max_length=64, blank=True, null=True)
    default_cost = models.FloatField()
    enable_prepaid_billing = models.PositiveIntegerField()
    credit = models.FloatField()
    callback_url = models.CharField(max_length=255, blank=True, null=True)
    simulate = models.IntegerField()
    simulate_deliver_every = models.PositiveIntegerField()
    simulate_permanent_failure_every = models.PositiveIntegerField()
    simulate_temporary_failure_every = models.PositiveIntegerField()
    simulate_mo_every = models.PositiveIntegerField()
    max_binds = models.PositiveIntegerField()
    connect_allow_ip = models.TextField(blank=True, null=True)
    dlt = models.CharField(max_length=5, blank=True, null=True)
    spam = models.IntegerField()
    reroute = models.CharField(max_length=10)
    coordinator = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'smpp_user'

class WordReplace(models.Model):
    id = models.BigAutoField(primary_key=True)
    word = models.CharField(max_length=100)
    replace_with = models.CharField(max_length=100)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'word_replace'
