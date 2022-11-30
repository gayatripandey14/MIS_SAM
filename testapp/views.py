from rest_framework.generics import GenericAPIView ,ListAPIView
# from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import  status
from rest_framework.response import Response
from rest_framework.views import *
from utils import permissions


# from .serializers import *
from django.db import transaction
from utils.permissions import IsResellerAdminSuperAdmin
from django.db.models import Q

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class TestView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        print(request.user.email,"---------")
        return Response({"working"})