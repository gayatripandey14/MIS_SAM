from rest_framework import serializers

class CampaignScheduleSerializer(serializers.Serializer):
    id = serializers.IntegerField(required = True)
    date = serializers.DateTimeField(required = True)
