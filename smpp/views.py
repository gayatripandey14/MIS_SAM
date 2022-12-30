# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import  status
from utils.funtions import validation_error

from utils.pagination import CustomPagination
from django.db.models import Q

from utils.permissions import *
from .utils import *
from .serializers import *
from .models import *
from users.models import AccountsUser as User
from testapp.models import  AccountsSmppusers,AccountsSmscroutes
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# class RouteCreateView(GenericAPIView):
#     permission_classes = (IsAuthenticated, IsAdminSuperAdminAgent, IsUserActive, )
#     serializer_class = RouteSerializer

#     def post(self, request):

#         serializer = self.serializer_class(data=request.data,context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         data = serializer.save()
#         return Response(data,status=status.HTTP_202_ACCEPTED)

#     custom_param = [

#             openapi.Parameter(name='id',
#                               in_=openapi.IN_QUERY,
#                               type=openapi.TYPE_INTEGER,
#                               description='get by id',
#                               required=False),
#             openapi.Parameter(name='page',
#                               in_=openapi.IN_QUERY,
#                               type=openapi.TYPE_INTEGER,
#                               description='Page No.',
#                               required=False),
#            ]
#     @swagger_auto_schema(manual_parameters = custom_param)
#     def get(self,request):
#         print("\n\n")

#         id = request.GET.get("id")

#         if id:
#             route_objs = AccountsSmscroutes.objects.filter(id=id)
#             print(route_objs)
#             count = route_objs.count()
#         else:
#             route_objs = get_master_routes(request.user)
#             route_objs.extend( get_children_routes(request.user) )
#             count = len(route_objs)


#         print("\n\n")
#         pagination = CustomPagination()
#         paginatedqs = pagination.paginate_queryset(route_objs, request)
#         serializer = RouteGetSerializer(paginatedqs, many=True)
#         return pagination.get_paginated_response(serializer.data,
#                                                  count)
    
#     def put(self,request):
#         id = request.data['id']
#         instance = AccountsSmscroutes.objects.filter(id=id,user=request.user.id,delete=False).first()
#         if instance is None:return Response(validation_error("you can't update this route"),status=400)
#         serializer = self.serializer_class(instance=instance,data=request.data,context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         data = serializer.save()
#         return Response(data,status=status.HTTP_202_ACCEPTED)

class RouteCreateView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminSuperAdminAgent, IsUserActive, )
    serializer_class = SmppSmscSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data,status=status.HTTP_202_ACCEPTED)

    custom_param = [

            openapi.Parameter(name='id',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='get by id',
                              required=False),
            openapi.Parameter(name='page',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='Page No.',
                              required=False),
           ]
    @swagger_auto_schema(manual_parameters = custom_param)
    def get(self,request):
        print("\n\n")

        id = request.GET.get("id")

        if id:
            route_objs = AccountsSmscroutes.objects.filter(id=id)
            print(route_objs)
            count = route_objs.count()
        else:
            route_objs = get_master_routes(request.user)
            route_objs.extend( get_children_routes(request.user) )
            count = len(route_objs)


        print("\n\n")
        pagination = CustomPagination()
        paginatedqs = pagination.paginate_queryset(route_objs, request)
        serializer = RouteGetSerializer(paginatedqs, many=True)
        return pagination.get_paginated_response(serializer.data,
                                                 count)
    
    def put(self,request):
        id = request.data['id']
        instance = AccountsSmscroutes.objects.filter(id=id,user=request.user.id,delete=False).first()
        if instance is None:return Response(validation_error("you can't update this route"),status=400)
        serializer = self.serializer_class(instance=instance,data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data,status=status.HTTP_202_ACCEPTED)

"""
super admin - Route - Admin - Agent

"""
class SmppUsersGetView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminSuperAdminAgent, IsUserActive, )
    serializer_class = SmppUsersSerializer

    def post(self,request):

        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data,status=status.HTTP_202_ACCEPTED)

    custom_param = [

            openapi.Parameter(name='id',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='get by id',
                              required=False),

            openapi.Parameter(name='user',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='get by id',
                              required=True),

            openapi.Parameter(name='page',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='Page No.',
                              required=False),
           ]

    @swagger_auto_schema(manual_parameters = custom_param)
    def get(self,request):
        print("\n\n")
        user = int(request.GET.get('user'))
        id = request.GET.get('id')
        user_obj = User.objects.filter(id=user).first()
        print(user_obj)
        if user_obj is None:
            return Response({'error':'does not exist'}, status=404)
        if id:route_obj = SmppUsers.objects.filter(id=id,assigned_to=user_obj.id,delete=False).order_by("-id")
        else:route_obj = SmppUsers.objects.filter(assigned_to=user_obj.id,delete=False).order_by("-id")
        """
        old logic
        if not request.GET.get('user'):
            user = request.user 
        else:
            user = User.objects.filter(id = request.GET['user']).first()

        if user is None: return Response({'error':'does not exist'}, status=404)
        if not check_if_parent(user, request.user): return Response({'error':'not a parent'}, status=401) 

        # if id:
            # route_obj = SmppUsers.objects.filter(user=user, id=id).first()
        print(f"getting all smpp users added by user --> {user.id} {user.user_type}")
        route_obj = SmppUsers.objects.filter(user=user.id).order_by("-id")
        """
        print("\n\n")
        pagination = CustomPagination()
        paginatedqs = pagination.paginate_queryset(route_obj, request)
        serializer = SmppUsersGetSerializer(paginatedqs, many=True)
        return pagination.get_paginated_response(serializer.data,
                                                 route_obj.count())


    custom_param = [
            openapi.Parameter(name='id',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='get by id',
                              required=False),
           ]

    @swagger_auto_schema(manual_parameters = custom_param)
    def delete(self, request):
        print("\n\n")
        smpp_id = request.GET.get('id')

        print(f"deleting --> AccountsSmppusers id : {smpp_id}")
        smpp_userobj = AccountsSmppusers.objects.get(id = smpp_id)
        smpp_userobj.delete = True
        smpp_userobj.save()
        """
        if not check_if_parent(smpp_userobj.user, request.user): return Response({'err' : 'not a parent'}, status=401)
        
        print(smpp_userobj)
        print(f"now deleting smpp_userdetails_id --> {smpp_userobj.smpp_userdetails_id}")

        user_details_obj = UserDetails.objects.get(id = smpp_userobj.smpp_userdetails_id)
        print(user_details_obj)

        user_details_obj.delete()
        smpp_userobj.delete()
        print("deleted.")
        """

        print("\n\n")
        return Response({'res' : 'deleted'}, status=200)

    def put(self,request):
        id = request.data['id']
        instance = SmppUsers.objects.filter(id=id,user=request.user.id,delete=False).first()
        if instance is None:return Response(validation_error("you can't update this route"),status=400)
        serializer = self.serializer_class(instance=instance,data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data,status=status.HTTP_202_ACCEPTED)




class SmppRouteListView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminSuperAdminAgent, IsUserActive, )
    serializer_class = RouteListSerializer
    custom_param = [

            openapi.Parameter(name='id',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='get by id',
                              required=False),
            openapi.Parameter(name='page',
                              in_=openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER,
                              description='Page No.',
                              required=False),
           ]
    @swagger_auto_schema(manual_parameters = custom_param)
    def get(self,request):
        print("\n\n")

        id = request.GET.get("id")

        if id:
            route_objs = AccountsSmscroutes.objects.filter(id=id)
        else:
            route_objs = AccountsSmscroutes.objects.all()
        serializer = self.serializer_class(route_objs,many=True)
        return Response(serializer.data)

            