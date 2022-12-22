
from .models import AccountsUser as User
from rest_framework_simplejwt.tokens import RefreshToken

import requests
from django.conf import settings
from django.core.exceptions import ValidationError

#code for otp verification begins
#for sending email otp verification
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from analytics.dbconnection import my_custom_sql
import datetime
GOOGLE_ID_TOKEN_INFO_URL = 'https://www.googleapis.com/oauth2/v3/tokeninfo'

def google_validate_id_token(*, id_token: str) -> bool:
    response = requests.get(
        GOOGLE_ID_TOKEN_INFO_URL,
        params={'id_token': id_token}
    )

    if not response.ok:
        raise ValidationError('id_token is invalid.')

    audience = response.json()['aud']

    if audience != settings.GOOGLE_OAUTH2_CLIENT_ID:
        raise ValidationError('Invalid audience.')

    return True

def phone_or_email_exists(request):
    phone_number = request.data.get('phone_number',None)
    email = request.data.get('email',None)
    
    if phone_number:
        user = User.objects.filter(phone_number=phone_number)
        if user.exists():
            return user.first() , "phone_number"

    if email:
        user = User.objects.filter(email=email)
        if user.exists():
            return user.first(), "email"

    else:
        return False , ''



def get_user_token(user):
    token = RefreshToken.for_user(user)
    return {"access":str(token.access_token),"refresh":str(token)}


# Code for MAIL

def generateOTP() :
    OTP = ''.join([str(random.randint(0,9)) for i in range(6)])
 
    return OTP

def get_mail_content(otp:str):
    mail_content = ""
    with open('templates/otp_verification_mail_template.html', 'r') as f:
        mail_content = f.read()
    mail_content = mail_content.replace('<h1 id="otp">23815</h1>',f'<h1 id="otp">{otp}</h1>')
    return mail_content

#function to generate email to send at any mail
def email_send(otp, email):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "OTP VERIFICATION"
    msg['From'] = 'no-reply@celetel.com'
    msg['To'] = email
    text = f"Your OTP is {otp}"
    html = get_mail_content(otp)
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("no-reply@celetel.com", "pfjdomiugpyknhux")
    s.sendmail('no-reply@celetel.com',email,msg.as_string())
    s.close()
#code for otp verification ends

#Here the code of verified otp Welcome mail starts
#function to read welcome mail html template
def welcome_mail_read():
    mail_content = ""
    with open('templates/welcome_mail_template.html', 'r') as f:
        mail_content = f.read()
    return mail_content

#function to create a welcome mail
def welcome_email_send(email):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Welcome to Celetel Technologies"
    msg['From'] = 'no-reply@celetel.com'
    msg['To'] = email
    html = welcome_mail_read()
    part = MIMEText(html, 'html')
    msg.attach(part)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("no-reply@celetel.com", "pfjdomiugpyknhux")
    s.sendmail('no-reply@celetel.com',email,msg.as_string())
    s.close()

    
 #Here the code of welcome mail is finished

def fetch_sms_cdr_table(start_date,end_date):
    sql = f"SELECT table_name FROM information_schema.tables WHERE TABLE_SCHEMA='kannel' AND table_name Like '%sms_cdr%' AND  date_format(create_time,'%Y-%m-%d %H:%M:%S') >= '{end_date}' AND date_format(create_time,'%Y-%m-%d %H:%M:%S') <= '{start_date}' "
    query = my_custom_sql(sql)  
    return query
def fetch_dlr_count(start_date,end_date):
    
    end = datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)
    end_date = end.strftime("%Y-%m-%d")
    tables = fetch_sms_cdr_table(start_date,end_date)
    rtn_data = []
    for data in tables:
        # query = f"SELECT (SELECT DISTINCT DISTINCT DATE(submit_time)  FROM {data['table_name']}) as submit_time,(SELECT Count(*)  FROM {data['table_name']}) as submission_count,(SELECT COUNT(*)  FROM {data['table_name']} WHERE status = 'UNDELIV') as undelivered_count,(SELECT COUNT(*)  FROM {data['table_name']} WHERE status = 'DELIVRD') as delivered_count "
        query = f"SELECT COUNT(*) AS submission_count,COUNT(CASE WHEN status = 'UNDELIV' THEN 1 END) AS undelivered_count,COUNT(CASE WHEN status = 'DELIVRD' THEN 1 END) AS delivered_count FROM {data['table_name']}"
        q = my_custom_sql(query)
        rtn_data.extend(q)  
    return rtn_data


def fetch_chart_data(start_date,end_date):
    
    tables = fetch_sms_cdr_table(start_date,end_date)
    rtn_data = []
    for data in tables:
        query = f"SELECT (SELECT DISTINCT DATE(submit_time)  FROM {data['table_name']}) as submit_time,(SELECT COUNT(*)  FROM {data['table_name']} WHERE status = 'DELIVRD') as delivered_count "
        # query = f"SELECT COUNT(*) AS delivered_count  FROM {data['table_name']} WHERE status = 'DELIVRD'"
        q = my_custom_sql(query)
        rtn_data.extend(q) 
    return rtn_data    