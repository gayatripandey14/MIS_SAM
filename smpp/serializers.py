from rest_framework import serializers
from testapp.models import AccountsSmscroutes as SmppSmscRoutes ,AccountsSmppusers as SmppUsers
from .models import SmppSmsc, SmppUser
from django.db.transaction import atomic
from users.models import AccountsUser as User
from django.forms import ValidationError
from .models import WordReplace
class SmppSmscSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmppSmsc
        fields = '__all__'





class RouteGetSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    details = serializers.SerializerMethodField()

    def get_user(self,obj):

        return User.objects.get(id=obj.user).email

    def get_details(self,obj):
        smpp_obj = SmppSmsc.objects.filter(id=obj.smpp_smsc_id)
        serailizer = SmppSmscSerializer(instance=smpp_obj,many=True)
        return serailizer.data

    class Meta:
        model = SmppSmscRoutes
        fields = ("id","creation_type","company","operator","price","date","country","user","details")



class RouteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    details = SmppSmscSerializer()
    class Meta:
        model = SmppSmscRoutes
        exclude = ("user","smpp_smsc_id","delete")

    def validate(self, attrs):
        """
        some validations
        """
        return super().validate(attrs)

    @atomic
    def update(self, instance, validated_data):
        smpp_data = validated_data.pop('details')
        smpp_instance = SmppSmsc.objects.get(id=instance.smpp_smsc_id)
        smpp_obj_serializer = SmppSmscSerializer(instance=smpp_instance,data=smpp_data)
        smpp_obj_serializer.is_valid(raise_exception=True)
        smpp_obj_serializer.save()
        SmppSmscRoutes.objects.filter(id=instance.id).update(**validated_data)
        validated_data['details'] = smpp_data
        validated_data['id'] = instance.id
        return validated_data

    @atomic
    def create(self, validated_data):

        """
        needs to be atomic for data consistency
        """

        smpp_data = validated_data.pop('details')
        smpp_obj_serializer = SmppSmscSerializer(data=smpp_data)
        smpp_obj_serializer.is_valid(raise_exception=True)
        smpp_obj = smpp_obj_serializer.save()
        obj = SmppSmscRoutes.objects.create(user=self.context['request'].user.id,smpp_smsc_id=smpp_obj.id,**validated_data)
        validated_data['details'] = smpp_data
        validated_data['id'] = obj.id

        return validated_data
    

class SmppUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = SmppUser
        fields = '__all__'

class SmppUsersGetSerializer(serializers.ModelSerializer):

    details = serializers.SerializerMethodField()

    def get_details(self,obj):
        '''
         smppuser id replace with system_id
        '''
        smpp_obj = SmppUser.objects.filter(system_id=obj.smpp_userdetails_id)
        serailizer = SmppUserSerializer(instance=smpp_obj,many=True)
        return serailizer.data
        
    class Meta:
        model = SmppUsers
        fields = ("id","route","details",)


class SmppUsersSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    details = SmppUserSerializer()

    class Meta:
        model = SmppUsers
        exclude = ("user","smpp_userdetails_id","delete")

    def validate(self, attrs):
        """
        some validations
        """
        try:
            user_obj = User.objects.get(id = attrs['assigned_to'])
        except:
            raise ValidationError("Invalid user")
        if user_obj.is_active == False:  raise ValidationError("Invalid user")

        return super().validate(attrs)
    @atomic
    def update(self, instance, validated_data):
        print(instance,"-----")
        """
        needs to be atomic for data consistency
        """
        validated_data.pop('route')
        validated_data.pop("assigned_to")
        '''
        id is systemid
        '''
        print(instance.smpp_userdetails_id)
        smppuser_instance = SmppUser.objects.get(system_id=instance.smpp_userdetails_id)
        smpp_user_data = validated_data.pop('details')
        dict_smpp_user= dict(smpp_user_data)
        smpp_obj_user_serializer = SmppUserSerializer(instance=smppuser_instance,data=smpp_user_data)
        smpp_obj_user_serializer.is_valid(raise_exception=True)
        smpp_obj_user_serializer.save()

        SmppUsers.objects.filter(id=instance.id).update(smpp_userdetails_id=dict_smpp_user['system_id'],**validated_data)

        validated_data['details'] = smpp_user_data
        validated_data['id'] = instance.id

        return validated_data


    @atomic
    def create(self, validated_data):


        """
        needs to be atomic for data consistency
        """
        smpp_user_data = validated_data.pop('details')
        smpp_obj_user_serializer = SmppUserSerializer(data=smpp_user_data)
        smpp_obj_user_serializer.is_valid(raise_exception=True)
        smpp_obj = smpp_obj_user_serializer.save()
        obj = SmppUsers.objects.create(user=self.context['request'].user.id,smpp_userdetails_id=smpp_obj.system_id,
                                    **validated_data)

        validated_data['details'] = smpp_user_data
        validated_data.pop('route')
        validated_data.pop("assigned_to")
        validated_data['id'] = obj.id

        return validated_data


class WordReplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordReplace     
        fields = ['id','word','replace_with','status']           