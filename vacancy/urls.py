from django.urls import path

from vacancy.views import *

app_name = "vacancy"
# app_name will help us do a reverse look-up latter.

urlpatterns = [
    # path('api/post/create', MessagesCreateAPI.as_view()),
    # path('api/post/get', DialogGetAPI.as_view()),
    # path('api/post/get', PostCreate.as_view()),
    # path('<int:pk>', PostView.as_view(), name='view'),
    path('', VacancyListView.as_view(), name='list'),
    path('<int:pk>', VacancyView.as_view(), name='item'),
    path('apply/', ApplyToVacancyView.as_view(), name='apply'),
    path('api/list/', VacancyListViewAPI.as_view(), name='vacancy-list-api'),
    # path('graph/<int:pk>', Graph.as_view(), name='graph'),
]