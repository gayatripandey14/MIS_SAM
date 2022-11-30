from rest_framework import serializers
from users.models import WalletWallet


class AddBalanceSerialzer(serializers.Serializer):
    amount = serializers.FloatField()
    service_id = serializers.IntegerField()



class WalletSerializer(serializers.ModelSerializer):
    service = serializers.SerializerMethodField()
    def get_service(self, obj):
        return obj.service.service.name

    class Meta:
        model = WalletWallet
        fields = "__all__"