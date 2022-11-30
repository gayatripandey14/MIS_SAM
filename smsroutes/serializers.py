from rest_framework import serializers
from users.models import *

class ServiceDetailsSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    def get_created_by(self, obj):
        return obj.created_by.email

    class Meta:
        model = ServicesServicedetail
        fields = ("id", "service_type", "name", "date", 'deduction_rate', "created_by")


class CreateServiceDetailsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = ServicesServicedetail
        exclude = ('created_by', 'expired', 'date', 'blocked')


class AssignRouteSerializer(serializers.Serializer):
    route_id = serializers.IntegerField(required=True)
    assign_to_user_id = serializers.IntegerField(required=True)
    deduction_rate = serializers.FloatField(required=True)



class GetAssignedRoutesSerializer(serializers.ModelSerializer):
    added_by = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    service = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()
    profit = serializers.SerializerMethodField()
    loss = serializers.SerializerMethodField()

    def get_balance(self,obj):
        return WalletWallet.objects.get(service=obj).balance

    def get_profit(self,obj):
        return WalletWallet.objects.get(service=obj).profit

    def get_loss(self,obj):
        return WalletWallet.objects.get(service=obj).loss

    def get_added_by(self, obj):
        return obj.added_by.email

    def get_user(self, obj):
        return obj.user.email

    def get_service(self, obj):
        return obj.service.name

    class Meta:
        model = ServicesServices
        fields = ("id","user","service","added_by","expiry_date","date","expired","balance","profit","loss")


class RemoveAssignedRouteSerializer(serializers.Serializer):
    services_service_id = serializers.IntegerField(required=True)