# Generated by Django 4.0.3 on 2022-11-14 11:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountsCompany',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('company_name', models.CharField(blank=True, max_length=200, null=True)),
                ('company_address', models.CharField(blank=True, max_length=200, null=True)),
                ('industry', models.CharField(blank=True, max_length=300, null=True)),
                ('contact_person', models.CharField(blank=True, max_length=200, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'accounts_company',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AccountsFinancialdetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('currency', models.CharField(blank=True, db_column='Currency', max_length=200, null=True)),
                ('credit_limit', models.FloatField(blank=True, null=True)),
                ('payment_terms', models.CharField(blank=True, max_length=20, null=True)),
                ('change_on', models.CharField(blank=True, max_length=50, null=True)),
                ('top_up', models.CharField(blank=True, max_length=50, null=True)),
                ('bank_method', models.CharField(blank=True, max_length=100, null=True)),
                ('notification', models.BooleanField()),
                ('threshold_amount', models.FloatField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=200, null=True)),
                ('low_balance_email', models.CharField(blank=True, max_length=200, null=True)),
                ('email_alert', models.BooleanField()),
            ],
            options={
                'db_table': 'accounts_financialdetail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AccountsOtherusersetting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pricing_email', models.CharField(blank=True, max_length=200, null=True)),
                ('finance_email', models.CharField(blank=True, max_length=200, null=True)),
                ('support_email', models.CharField(blank=True, max_length=200, null=True)),
                ('it_email', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.BooleanField()),
                ('agent_name', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'accounts_otherusersetting',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AccountsUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=datetime.datetime.now)),
                ('email', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=200, null=True)),
                ('user_type', models.CharField(max_length=20)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('otp', models.IntegerField(blank=True, null=True)),
                ('web_url', models.CharField(blank=True, max_length=300, null=True)),
                ('support_no', models.CharField(blank=True, max_length=200, null=True)),
                ('creation_type', models.CharField(max_length=20)),
                ('creation_id', models.CharField(blank=True, max_length=400, null=True)),
                ('otp_verified', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'accounts_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AccountsUserlog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('action', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField()),
            ],
            options={
                'db_table': 'accounts_userlog',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ServicesServicedetail',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('service_type', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('deduction_rate', models.FloatField()),
                ('expiry_date', models.DateTimeField(blank=True, null=True)),
                ('blocked', models.BooleanField(default=False)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 11, 14, 11, 3, 37, 442084))),
                ('expired', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'services_servicedetail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ServicesServices',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('deduction_rate', models.FloatField()),
                ('blocked', models.BooleanField(default=False)),
                ('expiry_date', models.DateTimeField(blank=True, null=True)),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 11, 14, 11, 3, 37, 442719))),
                ('expired', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'db_table': 'services_services',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ServicesServicesSmpp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'services_services_smpp',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ServicesSmpp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('tps', models.IntegerField(blank=True, null=True)),
                ('private', models.BooleanField()),
            ],
            options={
                'db_table': 'services_smpp',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WalletCampaignpassbook',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('campaign_id', models.IntegerField(blank=True, null=True)),
                ('campaign_name', models.CharField(blank=True, max_length=100, null=True)),
                ('volume', models.IntegerField(blank=True, null=True)),
                ('cost', models.FloatField()),
            ],
            options={
                'db_table': 'wallet_campaignpassbook',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WalletPassbook',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 11, 14, 11, 3, 37, 443944))),
                ('transanction_type', models.CharField(max_length=10)),
                ('amount', models.FloatField()),
                ('deduction_rate', models.FloatField()),
                ('available_balance', models.FloatField(default=0.0)),
            ],
            options={
                'db_table': 'wallet_passbook',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WalletWallet',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('balance', models.FloatField(default=0.0)),
                ('profit', models.FloatField(default=0.0)),
                ('loss', models.FloatField(default=0.0)),
            ],
            options={
                'db_table': 'wallet_wallet',
                'managed': False,
            },
        ),
    ]
