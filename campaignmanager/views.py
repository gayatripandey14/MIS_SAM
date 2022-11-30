from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import  status
from utils.funtions import validation_error
import json 
from mongoengine.errors import DoesNotExist
from smpp.utils import check_if_parent

from utils.permissions import * 
from users.models import AccountsUser
from .models import User, ComposeSMS, campaignSchedules
from .serializers import CampaignScheduleSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

class StopRunningCampaign(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminSuperAdminAgent, IsUserActive, )

    custom_param = [

            openapi.Parameter(name='camp_id',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='get by id',
                              required=False),

           ]

    @swagger_auto_schema(manual_parameters = custom_param)
    def delete(self, request):
        print("\n\n")
        camp_id = request.GET.get('camp_id')

        print(f"deleting camp_id --> {camp_id}")
        try: camp_obj = ComposeSMS.objects.get(id = camp_id)
        except DoesNotExist as e: return Response({'err' : e.__str__()}, status=404)

        camp_user = AccountsUser.objects.get(id = camp_obj.user.user_id)
        if not check_if_parent(child_user=camp_user, parent_user=request.user): 
            return Response({'err':'not a parent'}, status=401)

        camp_obj.status = 'Stopped'
        camp_obj.save()
        print("status changed to stopped.")

        print("\n\n")
        return Response({'res' : 'status changed to Stopped'}, status=200)

class GetCampaigns(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminSuperAdminAgent, IsUserActive, )

    custom_param = [

            openapi.Parameter(name='id',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='get by id',
                              required=True),

            openapi.Parameter(name='page',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='page number',
                              required=False),
            openapi.Parameter(name='camp_type',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_STRING,
                              description='campaign type',
                              required=False),

           ]

    @swagger_auto_schema(manual_parameters = custom_param)
    def get(self, request):
        id = request.GET.get('id')
        page = request.GET.get('page')
        camp_type = request.GET.get('camp_type')
        print("\n\n")

        print("YOU", request.user.email, request.user.user_type, sep=' -- ')

        if id: sel_user = AccountsUser.objects.get(id=id)
        else: sel_user = request.user
        print(f"selected user --> {sel_user.user_type}, {sel_user.email}")

        try: sel_mongo_user = User.objects.get(user_id = sel_user.id)  # 2, 3, 4, 21, 5, 6, 7, 11, 8, 9
        except DoesNotExist as e: return Response({'err' : e.__str__()}, status=404)
        # print( sel_mongo_user.to_json(indent=4) )

        if not camp_type:
            campaigns = ComposeSMS.objects.filter(user = sel_mongo_user).only(
                'id', 'user', 'message', 'date', 'campaing_name', 'numbers_to_send', 'total_sms', 'running', 'status'
            )
        else:
            # campaigns = ComposeSMS.objects.filter(status = camp_type)
            campaigns = ComposeSMS.objects.filter(user = sel_mongo_user, status = camp_type).only(
                'id', 'user', 'message', 'date', 'campaing_name', 'numbers_to_send', 'total_sms', 'running', 'status'
            )
        print(f"found {campaigns.count()} {camp_type} campaigns for user_id : {sel_user.id}")
        # print(campaigns[0].to_json(indent=4))

        rtrn_data = []
        for i, obj in enumerate(json.loads(campaigns.to_json(indent=4))):
            obj['user'] = sel_user.email
            obj['date'] = campaigns[i].date.strftime("%b %d %Y %H:%M:%S")
            rtrn_data.append(obj)


        print("\n\n")
        return Response(
            rtrn_data, 
            status=200
        )


class GetScheduledCampaigns(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminSuperAdminAgent, IsUserActive, )
    serializer_class = CampaignScheduleSerializer

    custom_param = [


            openapi.Parameter(name='page',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='page number',
                              required=False),
            openapi.Parameter(name='id',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='campaign id',
                              required=True),

           ]

    @swagger_auto_schema(manual_parameters = custom_param)
    def get(self, request):
        print("\n\n")
        camp_id = int(request.GET.get('id'))

        camp_schedules = campaignSchedules.objects.filter(
            composeSMS = camp_id, status = True
        ).only('date', 'composeSMS', 'draft')
        print(camp_schedules.to_json(indent=4))

        rtrn_data = []
        for i, obj in enumerate(json.loads(camp_schedules.to_json(indent=4))):
            obj['date'] = camp_schedules[i].date.strftime("%b %d %Y %H:%M:%S")
            rtrn_data.append(obj)

        print("\n\n")
        return Response(rtrn_data, status=200)

    custom_param = [


            openapi.Parameter(name='page',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='page number',
                              required=False),
            openapi.Parameter(name='id',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='schedule id',
                              required=True),

           ]

    @swagger_auto_schema(manual_parameters = custom_param)
    def delete(self, request):
        print("\n\n")
        schedule_id = int(request.GET.get('id'))

        camp_schedule = campaignSchedules.objects.get(id = schedule_id)
        camp_schedule.status = False
        camp_schedule.save()
        print("status changes to False.")

        print("\n\n")
        return Response({'res':"success"}, status=200)


    def put(self, request):
        print("\n\n")
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        schedule_id, schedule_date = serializer.data['id'], serializer.data['date']
        print(schedule_id, schedule_date)

        schedule_obj = campaignSchedules.objects.get(id = schedule_id)

        schedule_obj.date = schedule_date
        schedule_obj.save()

        rtrn_obj = json.loads(schedule_obj.to_json(indent=4))
        rtrn_obj['date'] = schedule_date

        print("\n\n")
        return Response(rtrn_obj, status=200)

    def post(self, request):
        print("\n\n")
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        camp_id, schedule_date = serializer.data['id'], serializer.data['date']
        schedule_obj = campaignSchedules(
            composeSMS = camp_id,
            date = schedule_date,
            status = True,
            draft = False
        ).save()

        rtrn_obj = json.loads(schedule_obj.to_json(indent=4))
        rtrn_obj['date'] = schedule_date


        print("\n\n")
        return Response(rtrn_obj, status=200)
