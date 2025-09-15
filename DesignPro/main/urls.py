from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('index/', views.index, name='index'),

    path('applications/create/', views.create_application, name='create_application'),
    path('applications/', views.application_list, name='application_list'),
    path('applications/delete/<int:pk>/', views.delete_application, name='delete_application'),
    path('applications/status/<int:pk>/', views.change_status, name='change_status'),

    path('categories/create/', views.create_category, name='create_category'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),

    path('staff/applications/', views.staff_application_list, name='staff_application_list'),
]
