from django.contrib import admin
from . import models


@admin.register(models.BusinessCard)
class BusinessCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'surname',  'work_email',  'field_of_activity', 'city', 'active', )
    list_filter = ('user', 'name', 'surname',  'work_email',  'field_of_activity', 'city', 'active', )
    list_editable = ('active', )
    search_fields = ('user', 'name', 'surname', 'work_email',  'field_of_activity', 'city',)


@admin.register(models.Telephone)
class TelephoneAdmin(admin.ModelAdmin):
    list_display = ('user', 'telephone', 'add_date', 'active', )
    list_filter = ('user', 'telephone', 'add_date', 'active', )
    list_editable = ('active', )
    search_fields = ('user', 'telephone', )


@admin.register(models.Social)
class SocialAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'icon', )


@admin.register(models.SocialNetworks)
class SocialNetworksAdmin(admin.ModelAdmin):
    list_display = ('user', 'social', 'username', 'add_date', 'active',)
    list_filter = ('user', 'social', 'username', 'add_date', 'active',)
    list_editable = ('active',)
    search_fields = ('user', 'username',)


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('user_from', 'user_to', 'created', )
    list_filter = ('user_from', 'user_to', 'created', )
    search_fields = ('user_from', 'user_to',)





