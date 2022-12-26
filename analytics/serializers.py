from dataclasses import fields
from email import message
from pyexpat import model
from rest_framework import serializers
from smpp.models import *
from testapp.models import AccountsSmppusers, AccountsSmscroutes

from users.models import AccountsUser
from .models import *
from .dbconnection import *
from datetime import timedelta
import datetime
import pytz
import time
from .utils import get_routes


class SmsLogSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = SmsCdr
        # fields = ['id','sender','receiver','dlr','err_code','msgid']
        fields = '__all__'



class CustomerAnalyticsSerializer(serializers.ModelSerializer):
    smsc_dlr = serializers.SerializerMethodField()

    
    def get_smsc_dlr(self,obj):
        if isinstance(obj,dict):
            smppuser = AccountsSmppusers.objects.filter(assigned_to=obj['id'])   
        else:  
            smppuser = AccountsSmppusers.objects.filter(assigned_to=obj.id)   
        user_dlr = [] 
        request = self.context.get('request')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        start = datetime.datetime.strptime(start_date, '%Y-%m-%d') + datetime.timedelta(days=1)
        start_date = start.strftime("%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)
        end_date = end.strftime("%Y-%m-%d")
        for user in smppuser:

            # user_detail = SmppUser.objects.filter(system_id=i.smpp_userdetails_id) 
            data = {}
            # for user in user_detail:  
            username =  user.smpp_userdetails_id
            dlr_count = sms_cdr_analytics(start_date,end_date,username) 
            
            data['username'] = username
            
            undelivered_count = 0
            delivered_count = 0
            submission_count = 0
            if dlr_count:
                for dlr in dlr_count:
                    undelivered_count= undelivered_count+dlr['undelivered_count']
                    delivered_count = delivered_count+dlr['delivered_count']
                    submission_count = submission_count+dlr['submission_count']

            data['undelivered_count'] = undelivered_count
            data['delivered_count'] = delivered_count
            data['submission_count'] = submission_count
            data['pending'] =  submission_count - (undelivered_count+delivered_count)
            if  data['submission_count']:
                data['delivery_rate'] = round(delivered_count/(submission_count)*100,2)
            

            user_dlr.append(data)
            
        return user_dlr
           

    class Meta:
        model = AccountsUser
        fields = ['email','smsc_dlr']



class SmscListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmppSmsc
        fields = ['smsc_id',]        

class RouteAnalyticsSerializer(serializers.ModelSerializer):
    smsc_dlr = serializers.SerializerMethodField()

    
    def get_smsc_dlr(self,obj):
        request = self.context.get('request')
        smsc_obj = AccountsSmscroutes.objects.filter(smpp_smsc_id=obj.id)     
        user_dlr = [] 
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        start = datetime.datetime.strptime(start_date, '%Y-%m-%d') + datetime.timedelta(days=1)
        start_date = start.strftime("%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)
        end_date = end.strftime("%Y-%m-%d")
        for route in smsc_obj:
            if request.user.user_type == 'Super Admin':smppuser = AccountsSmppusers.objects.filter(route=route.id)
            else:  smppuser = get_routes(request.user,route.id)
            for user_detail in smppuser:

                data = {}
                if request.user.user_type == 'Super Admin': username =  user_detail.smpp_userdetails_id
                else:username =  user_detail['username']
                data['username'] = username
                dlr_count = sms_cdr_analytics(start_date,end_date,username) 
                undelivered_count = 0
                delivered_count = 0
                submission_count = 0
                if dlr_count:
                    for dlr in dlr_count:
                        undelivered_count= undelivered_count+dlr['undelivered_count']
                        delivered_count = delivered_count+dlr['delivered_count']
                        submission_count = submission_count+dlr['submission_count']

                data['undelivered_count'] = undelivered_count
                data['delivered_count'] = delivered_count
                data['submission_count'] = submission_count
                data['pending'] =  submission_count - (undelivered_count+delivered_count)
                if  data['submission_count']:
                    data['delivery_rate'] = round(delivered_count/(submission_count)*100,2)
                user_dlr.append(data)
            
            
        return user_dlr
           

    class Meta:
        model = SmppSmsc
        fields = ['smsc_id','smsc_dlr']        

