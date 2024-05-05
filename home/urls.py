from django.urls import path, include

from . import views
from .views import login

urlpatterns = [
    path('', views.landing, name='landing'),
    path("home/admin/", include('loginas.urls')),
    path("", include('admin_material.urls')),
    path('home/accounts/login/', views.login_view, name='login_view'),
    path('signup/', views.signup_view, name='signup_view'),
    path('home/', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/images/', views.get_all_images, name='get_all_images'),
    path('file_history/', views.file_history, name='file_history'),
    path('create/', views.create_file, name='create_image'),
]
