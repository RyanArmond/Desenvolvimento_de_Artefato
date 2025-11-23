from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    #path('exemplo/', views.exemplo_view, name='exemplo_view'),

    path('', views.home, name='home_view')
]