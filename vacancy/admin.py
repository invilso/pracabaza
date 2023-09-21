from django.contrib import admin
from .models import State, City, Sex, InfoLabel, Category, Index, Photo, Video, WorkDuty, \
    HourlyPaymentOption, View, Vacancy
    
from tinymce.widgets import TinyMCE
from django.db import models


# Define Admin classes for your models
@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Sex)
class SexAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(InfoLabel)
class InfoLabelAdmin(admin.ModelAdmin):
    list_display = ('house', 'benefits')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
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

@admin.register(WorkDuty)
class WorkDutyAdmin(admin.ModelAdmin):
    list_display = ('description',)

@admin.register(HourlyPaymentOption)
class HourlyPaymentOptionAdmin(admin.ModelAdmin):
    list_display = ('payment_type', 'hourly_rate')

@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = ('ip', 'date_time', 'country', 'region_name', 'city', 'isp', 'mobile')

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'index', 'active', 'date_time', 'date_time_update')
    list_filter = ('city', 'state', 'category', 'sex')
    search_fields = ('name', 'city__name', 'index__name', 'category__name')

    filter_horizontal = ('photos', 'salary_per_hour', 'work_duties', 'sex', 'views')
    readonly_fields = ('embeded', 'views', 'date_time', 'date_time_update')
    
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'title', 'city', 'state', 'index', 'active')
        }),
        ('Медиа', {
            'fields': ('card_photo', 'photos', 'video', 'embeded')
        }),
        ('Описание и оплата', {
            'fields': ('info_label', 'salary_per_hour', 'salary_per_mounth_min', 'salary_per_mounth_max', 'salary_per_mounth_fixed', 'salary_per_hour_fixed', 'salary_is_netto')
        }),
        ('Детали и расписание', {
            'fields': ('work_duties', 'work_schedule', 'sex', 'category', 'description')
        }),
        ('Просмотры и метаданные', {
            'fields': ('views', 'date_time', 'date_time_update')
        }),
    )