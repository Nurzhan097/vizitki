from django.contrib import admin
from rest_auth.views import PasswordResetConfirmView
from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

API_TITLE = 'Blob API'
API_DESCRIPTION = 'A Weg API for creating and editing blog posts'
schema_view = get_schema_view(title=API_TITLE,
                              description=API_DESCRIPTION,
                              version='1.0.0')

urlpatterns = [
    path('api/', include('business_card_app.urls')),

    # auth
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/rest-auth/', include('rest_auth.urls')),
    # login/
    # {
    #     "username": "",
    #     "email": "",
    #     "password": ""
    # }
    # logout/
    # password/reset
    # {
    #     "email": ""
    # }
    #

    path('rest-auth/password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    # reset
    # {
    #     "new_password1": "",
    #     "new_password2": "",
    #     "uid": "",
    #     "token": ""
    # }

    # docs
    # pip install coreapi pyyaml
    path('schema/', schema_view),

    # получение документации
    path('docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION, public=False)),
    path('admin/', admin.site.urls),

    # registration
    path('api/v1/rest-auth/registration/', include('rest_auth.registration.urls')),
]
