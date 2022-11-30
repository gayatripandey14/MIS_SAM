from django.shortcuts import render

# Create your views here.
# Create your views here.
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import  status
from smpp.models import *
from utils.funtions import validation_error
from django.forms.models import model_to_dict

from utils.pagination import CustomPagination
from django.db.models import Q

from utils.permissions import *
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from .dbconnection import *
from testapp.models import *
from smpp.models import *
from smsroutes.utils import get_childrens,get_childrens_under_user
import datetime
from .serializers import CustomerAnalyticsSerializer, SmsLogSerializer,RouteAnalyticsSerializer,SmscListSerializer

class GetChildrensView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminSuperAdminAgent, IsUserActive, )
    
    def get(self,request):
        user = request.user
        children_obj = get_childrens(user)
        return Response(children_obj)



class GetChildrensUnderMeView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminSuperAdminAgent, IsUserActive, )
    
    def get(self,request):
        user = request.user
        children_obj = get_childrens_under_user(user)
        return Response(children_obj)        


class SmsLogView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminSuperAdminAgent, IsUserActive, )
    serializer_class = SmsLogSerializer

    custom_param = [openapi.Parameter(name='page',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              default=1,
                              required=False),
            openapi.Parameter(name='start_date',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING,
                              description='YYYY-MM-DD',
                              required=False),
            openapi.Parameter(name='end_date',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING,
                              description='YYYY-MM-DD',
                              required=False),
            openapi.Parameter(name='username',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING,
                              description='username',
                              required=False),]

    @swagger_auto_schema(manual_parameters = custom_param)

    def get(self,request):
        page = request.GET.get("page")
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        if start_date!=None and end_date!=None:
            
            start = datetime.datetime.strptime(start_date, '%Y-%m-%d') + datetime.timedelta(days=1)
            start_date = start.strftime("%Y-%m-%d")
            end = datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)
            end_date = end.strftime("%Y-%m-%d")
        username = request.GET.get("username")
        
        all = fetch_smslog_data(start_date,end_date,username,page)
        # serializer = self.serializer_class(all,many=True)

        # pagination = CustomPagination()
        # paginatedqs = pagination.paginate_queryset(serializer.data, request)
        # return pagination.get_paginated_response(paginatedqs,
        #                                         all.count(all))
   

        return Response(all)
        
       


class CustomerAnalyticsView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminSuperAdminAgent, IsUserActive, )

    serializer_class = CustomerAnalyticsSerializer
    custom_param = [openapi.Parameter(name='email',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING,
                              required=False),
                    openapi.Parameter(name='start_date',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING,
                              description='YYYY-MM-DD',
                              required=False),
                    openapi.Parameter(name='end_date',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING,
                              description='YYYY-MM-DD',
                              required=False),]

    @swagger_auto_schema(manual_parameters = custom_param)

    def get(self,request):
        email = request.GET.get("email")
        

        if email:
            account_user = AccountsUser.objects.get(email=email)   
            serializer = self.serializer_class(account_user,context={'request':request})

            return Response(serializer.data)
        else:
            # account_user = AccountsUser.objects.all() 
            account_user = get_childrens_under_user(request.user)
            serializer = self.serializer_class(account_user,many=True,context={'request':request})

            pagination = CustomPagination()
            paginatedqs = pagination.paginate_queryset(serializer.data, request)
            return pagination.get_paginated_response(paginatedqs,
                                                    account_user.count(account_user))
   



class SmscListVIEW(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminSuperAdminAgent, IsUserActive, )

    serializer_class = SmscListSerializer
    def get(self,request):
        smsc_obj = SmppSmsc.objects.all()
        serializer = self.serializer_class(smsc_obj,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class RouteAnalyticsView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminSuperAdminAgent, IsUserActive, )
    serializer_class = RouteAnalyticsSerializer
    custom_param = [openapi.Parameter(name='smsc_id',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING,
                              required=False),
                    openapi.Parameter(name='start_date',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING,
                              description='YYYY-MM-DD',
                              required=False),
                    openapi.Parameter(name='end_date',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING,
                              description='YYYY-MM-DD',
                              required=False),]

    @swagger_auto_schema(manual_parameters = custom_param)

    def get(self,request):
        smsc_id = request.GET.get("smsc_id")
        if smsc_id:
            smpp_smsc = SmppSmsc.objects.get(smsc_id=smsc_id)
            serializer = self.serializer_class(smpp_smsc,context={'request':request})
            return Response(serializer.data)
        else:    
            smpp_smsc = SmppSmsc.objects.all()

            serializer = self.serializer_class(smpp_smsc,many=True,context={'request':request})

            pagination = CustomPagination()
            paginatedqs = pagination.paginate_queryset(serializer.data, request)
            return pagination.get_paginated_response(paginatedqs,
                                                    smpp_smsc.count())
   