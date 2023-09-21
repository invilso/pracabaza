from django.urls import path

from .views import AboutUsView, LegalView, WarantyView, ContactsView

app_name = "info_pages"
# app_name will help us do a reverse look-up latter.

urlpatterns = [
    # path('api/post/create', MessagesCreateAPI.as_view()),
    # path('api/post/get', DialogGetAPI.as_view()),
    # path('api/post/get', PostCreate.as_view()),
    # path('<int:pk>', PostView.as_view(), name='view'),
    path('waranty/', WarantyView.as_view(), name='waranty'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('about-us/', AboutUsView.as_view(), name='about_us'),
    path('legal/<int:pk>', LegalView.as_view(), name='legal'),
    # path('graph/<int:pk>', Graph.as_view(), name='graph'),
]