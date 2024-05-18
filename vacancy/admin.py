from django.contrib import admin
from .models import Salary, State, City, Sex, InfoLabel, Category, Index, Photo, Video, WorkDuty, \
    HourlyPaymentOption, View, Vacancy, Requirement
    
from tinymce.widgets import TinyMCE
from django.db import models
from django.utils.translation import gettext as _
from modeltranslation.admin import TranslationAdmin

# Define Admin classes for your models
@admin.register(State)
class StateAdmin(TranslationAdmin):
    class Media:
        js = (
            'modeltranslation_jquery/jquery.min.js',
            'modeltranslation_jquery/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
    list_display = ('name',)

@admin.register(City)
class CityAdmin(TranslationAdmin):
    class Media:
        js = (
            'modeltranslation_jquery/jquery.min.js',
            'modeltranslation_jquery/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
    list_display = ('name',)

@admin.register(Sex)
class SexAdmin(TranslationAdmin):
    class Media:
        js = (
            'modeltranslation_jquery/jquery.min.js',
            'modeltranslation_jquery/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
    list_display = ('name',)

@admin.register(InfoLabel)
class InfoLabelAdmin(TranslationAdmin):
    class Media:
        js = (
            'modeltranslation_jquery/jquery.min.js',
            'modeltranslation_jquery/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
    list_display = ('house', 'benefits')

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    class Media:
        js = (
            'modeltranslation_jquery/jquery.min.js',
            'modeltranslation_jquery/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
    list_display = ('name',)

@admin.register(Index)
class IndexAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('file',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('file', 'url', 'embeded')
    

@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = ('ip', 'date_time', 'country', 'region_name', 'city', 'isp', 'mobile')

@admin.register(Vacancy)
class VacancyAdmin(TranslationAdmin):
    list_display = ('name', 'city', 'index', 'active', 'irrelevant', 'date_time', 'date_time_update')
    list_filter = ('city', 'state', 'category', 'sex')
    search_fields = ('name', 'city__name', 'index__name', 'category__name')

    filter_horizontal = ('photos', 'salary_per_hour', 'work_duties', 'requirements', 'sex', 'views')
    readonly_fields = ('embeded', 'views', 'date_time', 'date_time_update')
    
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
    
    class Media:
        js = (
            'modeltranslation_jquery/jquery.min.js',
            'modeltranslation_jquery/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

    fieldsets = (
        (_('Основная информация'), {
            'fields': ('name', 'title', 'city', 'state', 'index', 'active', 'irrelevant', 'with_experience')
        }),
        (_('Медиа'), {
            'fields': ('card_photo', 'photos', 'video', 'embeded')
        }),
        (_('Описание и оплата'), {
            'fields': ('info_label', 'salary_per_mounth_min', 'salary_per_mounth_max', 'salary_per_mounth_fixed', 'salary_per_hour_fixed', 'salary_is_netto', 'default_currency')
        }),
        (_('Детали и расписание'), {
            'fields': ('sex', 'category', 'description')
        }),
        (_('Просмотры и метаданные'), {
            'fields': ('views', 'date_time', 'date_time_update')
        }),
    )