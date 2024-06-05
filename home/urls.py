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
    path('history/', views.file_history, name='history'),
    # path('create/', views.create_file, name='create_image'),
     path('delete_template/<int:image_text_id>/', views.delete_template, name='delete_template'),
    path('search/', views.search, name='search'),
    path('write_dockerfile/', views.modify_dockerfile, name='write_dockerfile'),
    path('write_dockerfile/<int:file_id>/', views.modify_dockerfile, name='write_dockerfile_with_id'),
    # path('dockerhub_login/', views.dockerhub_login, name='dockerhub_login'),
    path('dockerfile_push/', views.dockerfile_push, name='dockerfile_push'),
    path('docker_compose/', views.docker_compose, name='docker_compose'),
    path('delete_template_editor/<int:image_text_id>/', views.delete_template_editor, name='delete_template_editor'),
    path('dockerfile_learn/', views.dockerfile_learn, name='dockerfile_learn'),
]