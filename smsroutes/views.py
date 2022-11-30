from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import  status
from utils.funtions import validation_error
from django.forms.models import model_to_dict

from utils.pagination import CustomPagination
from django.db.models import Q

from utils.permissions import *
from .serializers import *
from users.models import AccountsUser, ServicesServicedetail, ServicesServices
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken

from .utils import get_children_routes, get_master_routes, check_if_parent
# Create your views here.




class CreateRouteView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminSuperAdminAgent, IsUserActive, )
    serializer_class = CreateServiceDetailsSerializer

    def post(self, request):
        print(request.user.user_type)
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)

        routes = get_master_routes(request.user)
        routes.extend( get_children_routes(request.user) )

        for route in routes: 
            if route.name == request.data['name']: return Response({'err':'route with that name already exists'}, status=400) 

        ServicesServicedetail.objects.create(
            created_by = request.user,
            service_type = request.data['service_type'],
            name = request.data['name'],
            expiry_date = request.data.get('expiry_date'),
            description = request.data['description'],
            deduction_rate = request.data['deduction_rate'],
        )
        print("object created.")

        return Response(serializer.data, status=200)
    
    
    def put(self,request):

        id = request.data["id"]

        service_obj = ServicesServicedetail.objects.filter(id=id,created_by=request.user,expired = False).first()
        if service_obj is None:
            return Response(validation_error("you can't update this route"), status=400) 

        routes = get_master_routes(request.user)
        routes.extend( get_children_routes(request.user) )

        for route in routes: 

            if route.name == request.data['name']: return Response(validation_error("you can't update this route"), status=400) 

        serializer = self.serializer_class(instance=service_obj,data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=200)

    custom_param = [
            openapi.Parameter(name='id',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='id',
                              required=False),
           ]
    @swagger_auto_schema(manual_parameters = custom_param)
    def get(self, request):
        print("\n\n")
        id = request.GET.get("id")
        print("YOU", request.user.id, request.user.user_type, request.user.email, sep=" -- ", end='\n\n')

        if id:routes = ServicesServicedetail.objects.filter(id=id,expired = False)
        else:
            routes = get_master_routes(request.user)
            routes.extend( get_children_routes(request.user) )

        print("\n\n")

        pagination = CustomPagination()
        paginatedqs = pagination.paginate_queryset(routes, request)
        serializer = ServiceDetailsSerializer(paginatedqs, many=True)
        return pagination.get_paginated_response(serializer.data,
                                                 len(routes))


    custom_param = [
            openapi.Parameter(name='id',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='id',
                              required=True),
           ]
    @swagger_auto_schema(manual_parameters = custom_param)
    def delete(self,request):
        id = request.GET.get("id")

        service_obj = ServicesServicedetail.objects.filter(id=id,created_by=request.user).first()
        # print(ServicesServices.objects.filter().values())
        # return

        if service_obj is None:
            return Response(validation_error("you can't delete this route"), status=400) 

        service_obj.expired = True
        service_obj.save()

        ServicesServices.objects.filter(service=service_obj).update(expired=True)

        return Response({'res' : 'deleted'}, status=200)

class GetAssignedRoutesView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminSuperAdminAgent, IsUserActive, )
    serializer_class = GetAssignedRoutesSerializer

    def get(self, request, id):
        print("\n\n")

        sel_user = AccountsUser.objects.get(id = id)
        print(f"selected user --> {sel_user.user_type} {sel_user.email}")

        if not check_if_parent(sel_user, request.user): return Response({'err':'unauthorized'}, status=401)

        assigned_routes = ServicesServices.objects.filter(user = sel_user, expired=False)
        print(assigned_routes)

        print("\n\n")
        pagination = CustomPagination()
        paginatedqs = pagination.paginate_queryset(assigned_routes, request)
        serializer = GetAssignedRoutesSerializer(paginatedqs, many=True)
        return pagination.get_paginated_response(serializer.data,
                                                 assigned_routes.count())


class AssignRouteView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminSuperAdminAgent, IsUserActive, )
    serializer_class = AssignRouteSerializer


    def post(self, request):
        print("\n\n")

        print(request.user.user_type)
        serializer = AssignRouteSerializer(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)

        # check if this service is already assigned to this user

        sel_route = ServicesServicedetail.objects.get(id = request.data['route_id'])
        sel_user = AccountsUser.objects.get(id = request.data['assign_to_user_id'])
        print(f"assigning route '{sel_route.name}' to {sel_user.user_type} '{sel_user.email}'")

        ServicesServices.objects.create(
            deduction_rate = request.data['deduction_rate'],
            added_by = request.user,
            service = sel_route,
            user = sel_user,
        )
        print("object created.")

        print("\n\n")
        return Response({'res' : 'created'}, status=200)



class RemoveAssignedRouteView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminSuperAdminAgent, IsUserActive, )

    custom_param = [

            openapi.Parameter(name='service_id',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='services_service_id',
                              required=True),
           ]

    @swagger_auto_schema(manual_parameters = custom_param)
    def delete(self, request):
        print("\n\n")
        service_id = request.GET.get('service_id')

        print(request.user.user_type)

        service_obj = ServicesServices.objects.get(id = service_id)
        print(service_obj.added_by, service_obj.user, sep=' --> ')

        if not check_if_parent(child_user = service_obj.added_by, parent_user = request.user):
            return Response({'err':'not a parent'}, status=401)

        service_obj.expired = True
        service_obj.save()
        print("status of expired changed to True.")

        print("\n\n")
        return Response({'res' : 'deleted'}, status=200)