from django.contrib import admin
from .models import *
# Register your models here.
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('index' ,'name', 'views', 'state', 'city', 'category', 'active')  # Отображаемые поля в главном списке
    exclude = ('views',)  # Исключаем поле views из меню редактирования
    search_fields = ('title',)  # Поля для поиска
    list_filter = ('active', 'city__name', 'state__name')  # Фильтры
    def get_list_display_links(self, request, list_display):
        # Используем поле 'name' для ссылки открытия объекта
        return ('name', 'index')
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(City)
admin.site.register(Sex)
admin.site.register(InfoLabels)
admin.site.register(Category)
admin.site.register(State)
admin.site.register(Index)