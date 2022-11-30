
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import  status
from utils.funtions import validation_error
from django.forms.models import model_to_dict

from utils.pagination import CustomPagination
from django.db.models import Q
from .utils import walletlog

from utils.permissions import *
from .serializers import *
from users.models import  WalletWallet,ServicesServices
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken



class GetWalletView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsAdminSuperAdminAgent, IsUserActive, )
    serializer_class = AddBalanceSerialzer

    def post(self, request):
        print("\n\n")


        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        current_amount, service_id = serializer.data['amount'], serializer.data['service_id']


        wallet_obj = WalletWallet.objects.get(service = ServicesServices.objects.get(id=service_id) )

        previous_amount = wallet_obj.balance

        wallet_obj.balance = current_amount
        wallet_obj.save()

        walletlog(current_value=current_amount,previous_value=previous_amount,request=request,instance=wallet_obj)

        print("balance updated.")

        print("\n\n")
        return Response({'res':'success'}, status=200)


