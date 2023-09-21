from django.contrib import admin
from .models import Photo, PhoneNumber, SocialNetwork, ContactInfo, AboutUs, Guarantees, Partners, Team, LegalDocument
from tinymce.widgets import TinyMCE
from django.db import models

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('file', 'file_thumbnail_avatar', 'file_thumbnail_partner', 'file_thumbnail_guarantes')
    list_filter = ('file',)
    search_fields = ('file',)

@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('phone_number',)
    search_fields = ('phone_number',)

@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'link')
    list_filter = ('name',)
    search_fields = ('name',)

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('address',)
    filter_horizontal = ('phones', 'social_networks')
    search_fields = ('address',)
    readonly_fields = ('address_url',)

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('title', 'photo')
    search_fields = ('title',)
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

@admin.register(Guarantees)
class GuaranteesAdmin(admin.ModelAdmin):
    list_display = ('title', 'photo')
    list_filter = ('title',)
    search_fields = ('title',)

@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'photo')
    list_filter = ('name',)
    search_fields = ('name',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'photo')
    search_fields = ('name',)

@admin.register(LegalDocument)
class LegalDocumentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

# Дополнительные настройки административной панели могут быть добавлены здесь

