from dataclasses import fields
from rest_framework import serializers
from .models import AccountsUser as User, AccountsCompany as Company, AccountsFinancialdetail as FinancialDetail, AccountsOtherusersetting as OtherUserSetting
from django.db import transaction
import json
from django.forms import ValidationError
from .utils import *
import re
from django.contrib.auth.hashers import make_password

class AdminLoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField(max_length=200,required=False)
    # email = serializers.EmailField(max_length=50,required=False)
    password = serializers.CharField(max_length=200,required=False)
    
    def validate(self, attrs):
        password = attrs.get('password',None)
        email_or_phone = attrs['email_or_phone']
        check = bool(re.search("@",email_or_phone))
        if check:
            user_obj = User.objects.filter(email=email_or_phone).first()
        else:
            user_obj =User.objects.filter(phone_number=email_or_phone).first()
        print("user_obj",user_obj,"===")
        # if not user_obj or  not user_obj.check_password(password):
        
        if not user_obj:
            raise ValidationError("Invalid username or password.")
        else: 
            check_password = bool(user_obj.password == attrs['password'])
            print(check_password)
            if check_password:
                if user_obj.user_type in ['Reseller', 'User']:
                    raise ValidationError("unauthorized")
            else: raise ValidationError("invalid password. or username")
        
        return super().validate(attrs)

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        exclude = ('id',) 
 
              

class FinancialDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialDetail
        exclude = ('id',) 


class OtherUserSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherUserSetting
        # fields = '__all__'
        exclude = ('id',) 


class UserGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", 'phone_number', "user_type")



class UserSerializer(serializers.ModelSerializer):

    company= CompanySerializer()
    financial= FinancialDetailSerializer()
    other_data= OtherUserSettingSerializer()
    class Meta:
        model = User
        # fields = ("password","email","phone_number","user_type","company_data","financial_detail_data","other_detail_data") 
        exclude = ('id','support_no','first_name','last_name','address','date_joined','web_url','creation_type','creation_id','otp','created_by','last_login','is_active','is_superuser','is_staff','otp_verified','company_detail','financial_detail','other_detail')


    def validate(self, attrs):
        """
        some validations
        """
        user = self.context.get('request').user
        if user.user_type == "Super Admin" and "user_type" in attrs:
            user_type = attrs['user_type']
            if user_type == "Agent" or user_type=="User" or user_type=="Reseller" or user_type == "Admin":
                attrs['user_type'] = user_type
                
            else:
                attrs['user_type'] = 'User'

        if user.user_type == "Admin" and "user_type" in attrs:
            user_type = attrs['user_type']
            if user_type == "Agent" or user_type=="User" or user_type=="Reseller":
                attrs['user_type'] = user_type
                
            else:
                attrs['user_type'] = 'User'

        if user.user_type == "Agent" and "user_type" in attrs:
            user_type = attrs['user_type']
            if user_type == "User" or  user_type=="Reseller":
                attrs['user_type'] = user_type
                print(attrs['user_type'])
            else:
                attrs['user_type'] = 'User'        
                
        return super().validate(attrs)

    def create(self, validated_data):

        with transaction.atomic():
            """
            needs to be atomic for data consistency
            """

            company_data = validated_data.pop('company')
            financial_data = validated_data.pop('financial')
            other_data = validated_data.pop('other_data')

            company_data_serializer = CompanySerializer(data=company_data)
            company_data_serializer.is_valid(raise_exception=True)
            company_obj = company_data_serializer.save()
            

            financial_data_serializer = FinancialDetailSerializer(data=financial_data)
            financial_data_serializer.is_valid(raise_exception=True)
            finacial_obj = financial_data_serializer.save()
            

            other_data_serializer = OtherUserSettingSerializer(data=other_data)
            other_data_serializer.is_valid(raise_exception=True)
            other_obj = other_data_serializer.save()
            obj = User.objects.create(created_by=self.context['request'].user,company_detail=company_obj,financial_detail=finacial_obj,other_detail=other_obj,otp_verified=True,**validated_data)
            
            if validated_data['password']:
                # obj.set_password(validated_data['password'])
                validated_data['password'] = make_password(validated_data['password'])
                obj.password = validated_data['password']
                obj.save()
            validated_data['company_detail'] = company_data_serializer.data
            validated_data['financial_detail'] = financial_data_serializer.data
            validated_data['other_detail'] = other_data_serializer.data

            validated_data['id'] = obj.id 

        return validated_data



class GetUserSerializer(serializers.ModelSerializer):

    company_name = serializers.SerializerMethodField()
    financial_data = serializers.SerializerMethodField()
    other_data = serializers.SerializerMethodField()
    date_joined = serializers.SerializerMethodField()
    def get_company_name(self,obj):
        if obj.company_detail:
            return obj.company_detail.company_name
    def get_financial_data(self,obj):
        if obj.financial_detail:
            return {"currency":obj.financial_detail.currency,"credit_limit":obj.financial_detail.credit_limit}  

    def get_other_data(self,obj):
        if obj.other_detail:
            return {"status":obj.other_detail.status,"agent_name":obj.other_detail.agent_name}     
    def get_date_joined(self,obj):
        return obj.date_joined.strftime("%Y-%m-%d")            
    # def get_ccredit_limit(self,obj):
    #     if obj.financial_detail:
    #         return obj.financial_detail.currency            

    class Meta:
        model = User 
        exclude = ('password','phone_number','support_no','first_name','last_name','address','web_url','creation_id','otp','created_by','last_login','is_active','is_superuser','is_staff','otp_verified','company_detail','financial_detail','other_detail')
class GetnoUserSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()
    financial_data = serializers.SerializerMethodField()
    other_data = serializers.SerializerMethodField()
    # date_joined = serializers.SerializerMethodField()
    def get_company_name(self,obj):
        if obj["company_detail"]:
            return obj["company_detail"].company_name
    def get_financial_data(self,obj):
        if obj["financial_detail"]:
            return {"currency":obj["financial_detail"].currency,"credit_limit":obj["financial_detail"].credit_limit}  

    def get_other_data(self,obj):
        if obj['other_detail']:
            return {"status":obj['other_detail'].status,"agent_name":obj['other_detail'].agent_name}     
       
    class Meta:
        model = User 
        exclude = ('password','phone_number','support_no','first_name','last_name','address','web_url','creation_id','otp','created_by','last_login','is_active','is_superuser','is_staff','otp_verified')


class CustomerUpdateSerializer(serializers.ModelSerializer):
    company= CompanySerializer()
    financial= FinancialDetailSerializer()
    other_data= OtherUserSettingSerializer()
    class Meta:
        model = User
        
        # exclude = ('date_joined','created_by','otp','last_login','groups','is_active','is_superuser','is_staff','user_permissions','creation_type','creation_id')
        exclude = ('password','support_no','first_name','last_name','address','date_joined','web_url','creation_type','creation_id','otp','created_by','last_login','is_active','is_superuser','is_staff','otp_verified','company_detail','financial_detail','other_detail')
        
        # extra_kwargs = {
        #     'password': {'write_only': True},

        # }

    def validate(self, attrs):
        """
        some validations
        """
        user = self.context.get('request').user
        if user.user_type == "Super Admin" and "user_type" in attrs:
            user_type = attrs['user_type']
            if user_type == "Agent" or user_type=="User" or user_type=="Reseller" or user_type == "Admin":
                attrs['user_type'] = user_type
                
            else:
                attrs['user_type'] = 'User'

        if user.user_type == "Admin" and "user_type" in attrs:
            user_type = attrs['user_type']
            if user_type == "Agent" or user_type=="User" or user_type=="Reseller":
                attrs['user_type'] = user_type
                
            else:
                attrs['user_type'] = 'User'

        if user.user_type == "Agent" and "user_type" in attrs:
            user_type = attrs['user_type']
            if user_type == "User" or  user_type=="Reseller":
                attrs['user_type'] = user_type
                print(attrs['user_type'])
            else:
                attrs['user_type'] = 'User'        
                
        return super().validate(attrs)

    def update(self, instance, validated_data):
        print(instance.id)
        # user = self.context.get('request').user
        # user = User.objects.filter(id=instance.id).first()
        company_serializer = CompanySerializer(instance=instance.company_detail,data=validated_data['company'],partial=True)
        company_serializer.is_valid(raise_exception=True)
        company_serializer = company_serializer.save()

        financial_detail_serializer = FinancialDetailSerializer(instance.financial_detail,data=validated_data['financial'],partial=True)
        financial_detail_serializer.is_valid(raise_exception=True)
        financial_detail_serializer = financial_detail_serializer.save()
        
        other_deatil_serializer = OtherUserSettingSerializer(instance.other_detail,data=validated_data['other_data'],partial=True)
        other_deatil_serializer.is_valid(raise_exception=True)
        other_deatil_serializer = other_deatil_serializer.save()

        instance.email = validated_data.get("email", instance.email)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.user_type = validated_data.get("user_type", instance.user_type)
        instance.company_detail = company_serializer
        instance.financial_detail = financial_detail_serializer
        instance.other_detail = other_deatil_serializer

        instance.save()




        return super().update(instance, validated_data)        


        