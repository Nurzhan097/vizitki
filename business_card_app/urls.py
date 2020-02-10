from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


urlpatterns = (
    # v1
    # business cards
    path('v1/business-cards/<int:pk>', views.BusinessCardView.as_view()),  # get if pk(id usera)=0 тогла
                                                                           # берем данные пользователя
    path('v1/business-cards/', views.BusinessCardView.as_view()),  # get(all), post, put, delete

    # following
    path("v1/following/", views.FollowView.as_view()),
    path("v1/following/<int:pk>/", views.FollowView.as_view()),  # pk(user_id на которога подписан)

    # telephone
    path("v1/telephone/<int:pk>/", views.TelephoneView.as_view()),  # get pk-user_id(при=0 свои данные),
                                                                    # delete pk - id телефона
    path("v1/telephone/", views.TelephoneView.as_view()),  # post
    # v2
    path('v2/business-cards/', views.BusinessCardList.as_view()),
    path('v2/business-cards/<int:pk>/', views.BusinessCardDetail.as_view()),
)
