from django.db import models

class Cdr(models.Model):
    id = models.BigAutoField(primary_key=True)
    sender = models.CharField(max_length=64, blank=True, null=True)
    receiver = models.CharField(max_length=64, blank=True, null=True)
    dlr = models.CharField(max_length=160, blank=True, null=True)
    err_code = models.CharField(max_length=10, blank=True, null=True)
    msgid = models.CharField(max_length=64, blank=True, null=True)
    dlrtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'CDR'

class SmsCdr(models.Model):
    sql_id = models.PositiveBigIntegerField(primary_key=True)
    sender = models.CharField(max_length=20, db_collation='latin1_swedish_ci')
    receiver = models.CharField(max_length=20, db_collation='latin1_swedish_ci')
    content = models.TextField()
    submit_time = models.DateTimeField(blank=True, null=True)
    dlr_time = models.DateTimeField(blank=True, null=True)
    message_id = models.CharField(unique=True, max_length=255, db_collation='latin1_swedish_ci')
    account = models.CharField(max_length=255, db_collation='latin1_swedish_ci', blank=True, null=True)
    smsc = models.CharField(max_length=255, db_collation='latin1_swedish_ci', blank=True, null=True)
    parts = models.BigIntegerField(blank=True, null=True)
    entity_id = models.CharField(max_length=255, db_collation='latin1_swedish_ci', blank=True, null=True)
    content_id = models.CharField(max_length=255, db_collation='latin1_swedish_ci', blank=True, null=True)
    campaign = models.CharField(max_length=255, db_collation='latin1_swedish_ci', blank=True, null=True)
    status = models.CharField(max_length=255, db_collation='latin1_swedish_ci', blank=True, null=True)
    reason = models.TextField(db_collation='latin1_swedish_ci', blank=True, null=True)
    encoding = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sms_cdr'
