from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
    path('', views.ListView, name='list'),
    path('<int:id>', views.ItemView, name='item'),
    path('create/', views.create_view, name='create'),
    path('graph/<int:id>', views.plot_graph, name='graph')
]
if settings.DEBUG:  
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
