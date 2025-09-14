from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('index/', views.index, name='index'),
]
