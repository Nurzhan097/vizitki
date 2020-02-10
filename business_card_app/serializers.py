from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.contrib.auth import get_user_model
UserModel = get_user_model()
from . import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name', ]



class BusinessCardSerializer(serializers.Serializer):
    # id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255, allow_blank=True)
    surname = serializers.CharField(max_length=255, allow_blank=True)
    patronymic = serializers.CharField(max_length=255, allow_blank=True)
    work_email = serializers.CharField(max_length=255, allow_blank=True)
    position = serializers.CharField(max_length=255, allow_blank=True)
    company_name = serializers.CharField(max_length=255, allow_blank=True)
    field_of_activity = serializers.CharField(max_length=255, allow_blank=True)
    city = serializers.CharField(max_length=255, allow_blank=True)
    address = serializers.CharField(max_length=255, allow_blank=True)
    short_description = serializers.CharField(max_length=255, allow_blank=True)
    site = serializers.CharField(max_length=255, allow_blank=True)

    def create(self, validated_data, user_id=None):
        # print(validated_data)
        return models.BusinessCard.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.patronymic = validated_data.get('patronymic', instance.patronymic)
        instance.work_email = validated_data.get('work_email', instance.work_email)
        instance.position = validated_data.get('position', instance.position)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.field_of_activity = validated_data.get('field_of_activity', instance.field_of_activity)
        instance.city = validated_data.get('city', instance.city)
        instance.address = validated_data.get('address', instance.address)
        instance.short_description = validated_data.get('short_description', instance.short_description)
        instance.site = validated_data.get('site', instance.site)
        instance.active = True

        instance.save()
        return instance


class FollowingSerializer(serializers.Serializer):
    # business_card_id = serializers.IntegerField()
    user_from_id = serializers.IntegerField(write_only=True)
    user_to_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        return models.Contact.objects.create(**validated_data)


class TelephoneSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    telephone = serializers.CharField(max_length=15)

    def create(self, validated_data):
        return models.Telephone.objects.create(**validated_data)


class BusinessCardSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = models.BusinessCard
        fields = ('user_id',
                  'name',
                  'surname',
                  'patronymic',
                  'work_email',
                  'position',
                  'company_name',
                  'field_of_activity',
                  'city',
                  'address',
                  'short_description',
                  'site', )
        read_only_fields = ('user_id', )

        def create(self, validated_data):
            validated_data['user_id'] = self.request.user.id
            return models.BusinessCard.objects.create(**validated_data)










