from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    #path('exemplo/', views.exemplo_view, name='exemplo_view'),
    
    path('', views.home, name='home_view'),
    path('restaurante/', views.restaurante_view, name="restaurante_view"),
    path('login/', views.login_view, name='login'),
    path('login_google/', views.login_google_view, name='login_google'),
    path('logout/', views.logout_view, name='logout'),
    path('notas/', views.notas_view, name="notas_view"),
    path('profile/', views.profile_view, name='profile'),
]