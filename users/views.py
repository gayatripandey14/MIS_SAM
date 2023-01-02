from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import  status
from smpp.models import SmppSmsc,SmppUser
from utils.funtions import validation_error
from django.forms.models import model_to_dict

from utils.pagination import CustomPagination
from django.db.models import Q

from utils.permissions import *
from .serializers import *
from .models import AccountsUser as User, AccountsCompany as Company, AccountsFinancialdetail as FinancialDetail, AccountsOtherusersetting as OtherUserSetting
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
import datetime
import pandas as pd
from .utils import get_children_under_me
from smsroutes.utils import get_childrens_under_user

# from accounts.utils import *

# Create your views here.


class AdminLoginView(GenericAPIView):

    serializer_class = AdminLoginSerializer

    def post(self,request,):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            email_or_phone = serializer.data['email_or_phone']
            check = bool(re.search("@",email_or_phone))
            
            if check:
                user_obj = User.objects.get(email=email_or_phone)
            else:
                user_obj =User.objects.get(phone_number=email_or_phone)
            print("\n\n", user_obj, "\n\n")
            
            token = get_user_token(user_obj)
            return Response(token,status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(validation_error("Invalid Username or password"),status=status.HTTP_400_BAD_REQUEST)

class CustomerCreateView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminSuperAdminAgent, IsUserActive, )
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data,status=status.HTTP_202_ACCEPTED)


    def get(self,request):
        if self.request.user.user_type=="Super Admin":
            users = User.objects.filter(is_active=True)
            pagination = CustomPagination()
            paginatedqs = pagination.paginate_queryset(users, request)
            serializer = GetUserSerializer(paginatedqs, many=True)
            return pagination.get_paginated_response(serializer.data,
                                                    users.count())
        else:
            users = get_children_under_me(request.user)
            count = len(users)
            pagination = CustomPagination()
            paginatedqs = pagination.paginate_queryset(users, request)
            serializer = GetnoUserSerializer(paginatedqs, many=True)
            return pagination.get_paginated_response(serializer.data,
                                                    count)
        
        # if self.request.user.user_type=="Admin":
        #     users = User.objects.filter(created_by=request.user,is_active=True)
        #     # user = User.objects.filter(Q(created_by=request.user) | Q(user_type="Agent") | Q(user_type="User") | Q(user_type="Reseller"),is_active=True)
        #     # user = User.objects.filter(Q(created_by=request.user) | Q(user_type="Agent"),is_active=True)
            
        #     # ids_list = []
        #     # user_obj_list = []

        #     # for i in user:
        #     #     ids_list.append(i.id)
        #     #     user_obj_list.append(i)

        #     # users = User.objects.filter(Q(id__in=ids_list) | Q(created_by__in = user_obj_list),is_active=True)

        # if self.request.user.user_type=="Agent":
        #     users = User.objects.filter(Q(user_type="User") | Q(user_type="Reseller"),created_by=request.user,is_active=True)

        # print("\n\n")
        # print(users)
        # print("\n\n")

        # user_data = []
        # for user in users:
        #     print(user)
        #     user_dict={}
        #     user_dict['email'] = user.email
        #     user_dict['user_id'] = user.id
        #     user_dict['created_by'] = user.created_by.id
        #     user_dict['creation_time'] = user.date_joined
        #     user_dict['currency'] = user.financial_detail.currency
        #     user_dict['credit_limit'] = user.financial_detail.credit_limit
        #     user_dict['company_name'] = user.company_detail.company_name
        #     user_dict['agent_name'] = user.other_detail.agent_name
        #     user_dict['status'] = user.other_detail.status




        #     user_data.append(user_dict)
        # pagination = CustomPagination()
        # paginatedqs = pagination.paginate_queryset(user_data, request)
        # # serializer = UserSerializer(paginatedqs, many=True)
        # return pagination.get_paginated_response(paginatedqs,users.count())
                       

    
    
class CustomerDetailView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminSuperAdminAgent, IsUserActive, )

    serializer_class = CustomerUpdateSerializer

    def get(self, request, id):
        print("\n\n")
        print("YOU", request.user.id, request.user.first_name, sep=' -- ')

        try: sel_user = User.objects.get(id=id)
        except: return Response({'err':'does not exist'}, status=404)

        # if not sel_user.created_by == request.user:
            # return Response({'err' : 'not created by you'}, status=400)


        rtrn_data = {
            'email' : sel_user.email,
            'phone_number' : sel_user.phone_number,
            'user_type' : sel_user.user_type
        }
        rtrn_data['company'] = model_to_dict(sel_user.company_detail)
        rtrn_data['financial'] = model_to_dict(sel_user.financial_detail)
        rtrn_data['other_data'] = model_to_dict(sel_user.other_detail)
        del rtrn_data['company']['id']
        del rtrn_data['financial']['id']
        del rtrn_data['other_data']['id']

        print("\n\n")
        return Response(rtrn_data, status=200)

    
    def patch(self, request, id=None):
        user = User.objects.filter(id=id).first()
        # company_serializer = CompanySerializer(instance=user.company_detail,data=request.data['company'],partial=True)
        # company_serializer.is_valid(raise_exception=True)
        # company_serializer = company_serializer.save()

        # financial_detail_serializer = FinancialDetailSerializer(user.financial_detail,data=request.data['financial'],partial=True)
        # financial_detail_serializer.is_valid(raise_exception=True)
        # financial_detail_serializer = financial_detail_serializer.save()
        
        # other_deatil_serializer = OtherUserSettingSerializer(user.other_detail,data=request.data['other_data'],partial=True)
        # other_deatil_serializer.is_valid(raise_exception=True)
        # other_deatil_serializer = other_deatil_serializer.save()


        # # user.email = request.data['email']
        # # user.phone_number = request.data['phone_number']

        # # user.user_type = request.data['user_type']
        # # user.company_detail = company_serializer
        # # user.financial_detail = financial_detail_serializer
        # # user.other_detail = other_deatil_serializer

        # # user.save()
        serializer = self.serializer_class(instance=user,data=request.data,partial=True,context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request, id=None):
        try:
            if request.user.user_type == "Super Admin":
                user = User.objects.filter(Q(user_type="Admin") | Q(user_type="Agent") | Q(user_type="User")|Q(user_type="Reseller"),id=id).first()
            if request.user.user_type == "Admin":
                user = User.objects.filter(Q(user_type="Agent") | Q(user_type="User") | Q(user_type="Reseller"),id=id,created_by=request.user).first()
                
            if request.user.user_type == "Agent":
                user = User.objects.filter(Q(user_type="User") | Q(user_type="Reseller"),id=id,created_by=request.user).first()
            user.is_active = False
            user.save()
            return Response("User Deleted Successfully")
        except Exception as e:
            return Response(validation_error(str(e)),status=status.HTTP_400_BAD_REQUEST)    




class GetCustomersUnderMeView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminSuperAdminAgent, IsUserActive, )
    serializer_class = UserSerializer

    custom_param = [openapi.Parameter(name='search',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING,
                              description='Search of records in a page',
                              required=False),
            openapi.Parameter(name='page',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='Page number',
                              required=False),
            openapi.Parameter(name='filter',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING,
                              description='select user_type filter',
                              required=False),
            openapi.Parameter(name='id',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='select user_id',
                              required=False),
            ]

    @swagger_auto_schema(manual_parameters = custom_param)
    def get(self, request):
        print("\n\n")

        user_filter = request.GET.get("filter")
        user_id = request.GET.get("id")

        # print("YOU", request.user.id, request.user.first_name, sep=' -- ')

        if user_id:
            selected_user = User.objects.get(id=user_id)
            emp_under_me = User.objects.filter(created_by = selected_user, is_active=True)
        else:
            emp_under_me = User.objects.filter(created_by = request.user, is_active=True)

        if user_filter:
            emp_under_me = emp_under_me.filter(user_type = user_filter)

        pagination = CustomPagination()
        paginatedqs = pagination.paginate_queryset(emp_under_me, request)
        serializer = UserGetSerializer(paginatedqs, many=True)
        return pagination.get_paginated_response(serializer.data,
                                                 emp_under_me.count())


class DashBoardView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminSuperAdminAgent, IsUserActive, )
    custom_param = [openapi.Parameter(name='query',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING,
                              description='Query parameter',
                              required=False),
                    openapi.Parameter(name='filter',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING,
                              description=' ',
                              required=False),        
                    openapi.Parameter(name='Initial_date',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING,
                              description='YYYY-MM-DD',
                              required=False),
                    openapi.Parameter(name='Final_date',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING,
                              description='YYYY-MM-DD',
                              required=False),]       

    @swagger_auto_schema(manual_parameters = custom_param)
    def get(self,request):
        filter = request.GET.get('filter',None)
        query = request.GET.get('query',None)
        Initial_date = request.GET.get('Initial_date',None)
        Final_date = request.GET.get('Final_date',None)


        
        system_id = SmppSmsc.objects.all().count()
        route = SmppUser.objects.all().count()
        total_user = len(get_childrens_under_user(request.user))
        # users = AccountsUser.objects.filter(created_by = request.user).count()
        if query == 'DeliveryCount':
            if filter == "ThisDay":
                start_date = datetime.datetime.now().strftime("%Y-%m-%d")
                end_date =datetime.datetime.now() - datetime.timedelta(days=1)
                end_date = end_date.strftime("%Y-%m-%d")
                undelivered_count = 0
                delivered_count = 0
                submission_count = 0
                all = fetch_dlr_count(start_date,end_date)
                for i in all:
                    undelivered_count = undelivered_count+i['undelivered_count']
                    delivered_count = delivered_count+i['delivered_count']
                    submission_count = submission_count+i['submission_count']
                if submission_count == 0:
                    successrate = 0
                else:
                    successrate = delivered_count/submission_count * 100
                count_dict = {"system_id":system_id,'route':route,'total_user':total_user,
                            'undelivered_count':undelivered_count,
                            'delivered_count':delivered_count,
                            'total':submission_count,
                            'successrate':round(successrate,2)}
               
                return Response(count_dict)

            if filter == "ThisWeek":
                start_date = datetime.datetime.now().strftime("%Y-%m-%d")
                end_date =datetime.datetime.now() - datetime.timedelta(days=7)
                end_date = end_date.strftime("%Y-%m-%d")
                
                undelivered_count = 0
                delivered_count = 0
                submission_count = 0
                all = fetch_dlr_count(start_date,end_date)
                
                for i in all:
                    undelivered_count = undelivered_count+i['undelivered_count']
                    delivered_count = delivered_count+i['delivered_count']
                    submission_count = submission_count+i['submission_count']
                if submission_count == 0:
                    successrate = 0

                successrate = delivered_count/submission_count * 100
                count_dict = {"system_id":system_id,'route':route,
                            'undelivered_count':undelivered_count,
                            'delivered_count':delivered_count,
                            'total':submission_count,
                            'successrate':round(successrate,2)}

                return Response(count_dict)   

            if filter == "ThisMonth":
                start_date = datetime.datetime.now().strftime("%Y-%m-%d")
                end_date =datetime.datetime.now() - datetime.timedelta(days=30)
                end_date = end_date.strftime("%Y-%m-%d")

                undelivered_count = 0
                delivered_count = 0
                submission_count = 0

                all = fetch_dlr_count(start_date,end_date)
                
                for i in all:
                    undelivered_count = undelivered_count+i['undelivered_count']
                    delivered_count = delivered_count+i['delivered_count']
                    submission_count = submission_count+i['submission_count']
                if submission_count == 0:
                    successrate = 0

                successrate = delivered_count/submission_count * 100
                count_dict = {"system_id":system_id,'route':route,
                            'undelivered_count':undelivered_count,
                            'delivered_count':delivered_count,
                            'total':submission_count,
                            'successrate':round(successrate,2)}
                
                return Response(count_dict)    
        if query == 'AnalyticsData':
            if filter.startswith('messages_days'):

                days = int(filter.replace('messages_days', ''))  
                start_date = datetime.datetime.now()
                end_date =datetime.datetime.now() - datetime.timedelta(days=days)
                rtrn = {}
                for single_date in pd.date_range(end_date, start_date):
                    rtrn[str(single_date.date())] = 0
                campaign_analytics = fetch_chart_data(start_date,end_date)
                for obj in campaign_analytics:
                    if obj['submit_time'] != None:
                        # print(rtrn[ str(obj['submit_time']) ])
                        rtrn[ str(obj['submit_time']) ] = rtrn[ str(obj['submit_time']) ] + obj['delivered_count']
                rtrn_list = []
                for i in list(rtrn):
                    rtrn_list.append( {
                        "date" : str(i),
                        "delivered_messages" : rtrn[i]
                    } )
                return Response(rtrn_list)    

            if filter.startswith('messages_month'):

                months = int(filter.replace('messages_month', ''))  
                start_date = datetime.datetime.now() 
                end_date =datetime.datetime.now() - datetime.timedelta(days=months*30)
                start_date = start_date.strftime("%Y-%m-%d")
                end_date = end_date.strftime("%Y-%m-%d")
                rtrn = {}
                for single_date in pd.date_range(end_date, start_date, freq='MS'):
                    rtrn[f"{single_date.date().strftime('%B')}-{single_date.date().year}"] = 0

                campaign_analytics = fetch_chart_data(start_date,end_date)
                
                for obj in campaign_analytics:
                    if obj['submit_time'] != None:
                        month_yr = f"{obj['submit_time'].strftime('%B')}-{obj['submit_time'].year}"
                        rtrn[ month_yr ] = rtrn[ month_yr ] + obj['delivered_count']
                
                rtrn_list = []
                for i in list(rtrn):
                    rtrn_list.append( {
                        "date" : str(i),
                        "delivered_messages" : rtrn[i]
                    } )
                return Response(rtrn_list)   

            '''
            Chart 
            
            '''
            if filter == "SelectRange":
                format = "%Y-%m-%d" # The format
                Initial_date = datetime.datetime.strptime(Initial_date,format)
                Final_date = datetime.datetime.strptime(Final_date,format)

                
                if (
                    Initial_date.date() < datetime.date(2015, 1, 1) or
                    Final_date.date() > datetime.date(2027, 1, 1)
                ): 
                    return {"error" : "invalid date range"}

            delta = Final_date.date() - Initial_date.date()
            
            rtrn = {}
            if delta.days < 365:
                for single_date in pd.date_range(Initial_date, Final_date):
                    rtrn[single_date.date()] = 0
                campaign_analytics = fetch_chart_data(Final_date+datetime.timedelta(days=2),Initial_date+datetime.timedelta(days=1))

                for obj in range(1,len(campaign_analytics)):
                    if campaign_analytics[obj]['submit_time'] != None:
                        rtrn[ campaign_analytics[obj]['submit_time'] ] = rtrn[ campaign_analytics[obj]['submit_time'] ] + campaign_analytics[obj]['delivered_count']
                
                # for obj in campaign_analytics:
                #     print(f"_____________________submit_date{obj['submit_time']}")
                #     if obj['submit_time'] != None:
                #         rtrn[ obj['submit_time'] ] = rtrn[ obj['submit_time'] ] + obj['delivered_count']
                
            else:
                for single_date in pd.date_range(Initial_date, Final_date, freq='MS'):
                    rtrn[f"{single_date.date().strftime('%B')}-{single_date.date().year}"] = 0
                '''
                    To Fetch data from Mysql
                '''
                campaign_analytics = fetch_chart_data(Final_date,Initial_date)

                for obj in range(1,len(campaign_analytics)):
                    if campaign_analytics[obj]['submit_time'] != None:
                        month_yr = f"{campaign_analytics[obj]['submit_time'].strftime('%B')}-{campaign_analytics[obj]['submit_time'].year}"
                        rtrn[ month_yr ] = rtrn[ month_yr ] + campaign_analytics[obj]['delivered_count']
                        
            rtrn_list = []
            for i in list(rtrn):
                rtrn_list.append( {
                    "date" : str(i),
                    "delivered_messages" : rtrn[i]
                } )

            
            return Response(rtrn_list)

    