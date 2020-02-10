from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth import get_user_model

UserModel = get_user_model()

from . import models, serializers


# API/V1
class BusinessCardView(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            # Получаем одну визитку
            if pk == 0:
                pk = request.user.pk
            try:
                # Вывод визитки
                business_card = models.BusinessCard.objects.filter(active=True, user__id=pk)
                serializer = serializers.BusinessCardSerializer(business_card, many=True)
                return Response({'business_card': serializer.data})
            except(TypeError, ValueError, OverflowError, models.BusinessCard.DoesNotExist):
                return Response({'error': "Business card not found"})
        else:
            # Получаем все визитки находящиеся в избранных
            followers_contact = models.Contact.objects.filter(user_from=request.user).exclude(user_to=request.user)
            business_cards = models.BusinessCard.objects.filter(user__rel_to_set__in=followers_contact,
                                                                active=True).distinct()
            business_cards.order_by("-user__following__created")
            serializer = serializers.BusinessCardSerializer(business_cards, many=True)
            return Response({'business_cards': serializer.data})

    def post(self, request, pk = None):
        try:
            pk = models.BusinessCard.objects.get(user=request.user).pk
        except(TypeError, ValueError, OverflowError, models.BusinessCard.DoesNotExist):
            pk = None

        if pk:
            return self.put(request)
        else:
            # Если у пользователя нет визитки
            business_card = request.data.get('business_card')
            print(business_card)
            business_card["user_id"] = request.user.id
            serializer = serializers.BusinessCardSerializer(data=business_card)
            if serializer.is_valid(raise_exception=True):
                business_card_saved = serializer.save(user_id=request.user.id)
            return Response({"success": f"Business card {business_card_saved} created successfully."})

    def put(self, request, pk = None):
        pk = models.BusinessCard.objects.get(user=request.user).pk
        saved_business_card = models.BusinessCard.objects.get(pk=pk)
        data = request.data.get('business_card')
        serializer = serializers.BusinessCardSerializer(instance=saved_business_card,
                                                        data=data,
                                                        partial=True)  # возможность обновлять только некоторые поля
        if serializer.is_valid(raise_exception=True):
            business_card_saved = serializer.save()
        return Response({
            "success": f"Business card {business_card_saved} update successfully.",
        })

    def delete(self, request, pk = None):
        user = request.user
        business_card = models.BusinessCard.objects.get(user=user)
        business_card.delete()
        # business_card.save()
        # Удаляет все на него подписки
        contact = models.Contact.objects.filter(user_to=user)
        contact.delete()
        # Удаляет все телефоны
        telephone = models.Telephone.objects.filter(user=user)
        telephone.delete()
        # Удаляет все соцсети
        social_networks = models.SocialNetworks.objects.filter(user=user)
        social_networks.delete()
        return Response({"message": f"Business card {business_card} has been deleted."})


#  card
{
    "business_card":
        {

            "name": "Имя123",
            "surname": "11",
            "patronymic": "",
            "work_email": "atar.7@gmail.com",
            "position": "Backend",
            "company_name": "",
            "field_of_activity": "",
            "city": "",
            "address": "",
            "short_description": "",
            "site": ""
        }
}


class FollowView(APIView):
    def post(self, request, pk = None):
        user_from = request.user
        following_data = request.data.get('following_data')
        following_data["user_from_id"] = user_from.id

        serializer = serializers.FollowingSerializer(data=following_data)
        if serializer.is_valid(raise_exception=True):
            following_saved = serializer.save()
        return Response({"success": f"{following_saved} successfully."})

    def delete(self, request, pk=None):
        if pk is not None:
            user_from_id = request.user.pk
            user_to_id = pk
            contact = models.Contact.objects.filter(user_from=user_from_id, user_to=user_to_id)
            # print(contact)
            contact.delete()
            return Response({"message": "unfollow successfully"})
        return Response({"error": "Following user parameter was not sent"})

{
    "following_data":
        {
            "user_to_id": "2"
        }
}




# Telephone
class TelephoneView(APIView):
    def get(self, requset, pk=0):
        if pk == 0:
            pk = requset.user.pk
        try:
            telephones = models.Telephone.objects.filter(user=pk)
            serializer = serializers.TelephoneSerializer(telephones, many=True)
            return Response({"telephones": serializer.data})
        except(TypeError, ValueError, OverflowError, models.Telephone.DoesNotExist):
            return Response({'error': "Telephones not found"})

    def post(self, request):
        telephone_data = request.data.get('telephone_data')
        telephone_data["user_id"] = request.user.pk
        serializer = serializers.TelephoneSerializer(data=telephone_data)
        if serializer.is_valid(raise_exception=True):
            telephone_saved = serializer.save()
        return Response({"success": f"Telephone {telephone_saved} successfully created."})

    def delete(self, request, pk=None):
        if pk is not None:
            try:
                telephone = models.Telephone.objects.get(user=request.user, id=pk)
                telephone.delete()
                return Response({'message': f'Telephone {telephone} deleted successfully.'})
            except Exception:
                return Response({'error': f'Telephone not found'})


{
    "telephone_data":
        {
            "telephone": "5454646213"
        }
}


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer




# API/V2
class BusinessCardList(generics.ListCreateAPIView):
    # queryset = models.BusinessCard.objects.filter(user_from=self.request.user).exclude(user_to=request.user)
    serializer_class = serializers.BusinessCardSerializerV2

    def get_queryset(self):
        followers_contact = models.Contact.objects.filter(user_from=self
                                                          .request.user).exclude(user_to=self.request.user)
        business_cards = models.BusinessCard.objects.filter(user__rel_to_set__in=followers_contact,
                                                            active=True).distinct()
        return business_cards

class BusinessCardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.BusinessCard.objects.all()
    serializer_class = serializers.BusinessCardSerializerV2

    def perform_create(self, serializer):
        queryset = models.BusinessCard.objects.filter(user=self.request.user)
        if queryset.exists():
            raise ValidationError('You have already signed up')
        serializer.save(user=self.request.user)



