from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<city>', views.detail_city, name='detail_city'),
    path('delete/<city>', views.delete_city, name='delete_city'),
]
