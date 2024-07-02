from django.urls import path, include

from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import password_reset_request
from django.views.generic import RedirectView

urlpatterns = [
    path('accounts/login/', RedirectView.as_view(url='/login/')),
    path('', views.landing, name='landing'),
   path("", include('admin_material.urls')),
    path('login/', views.login_view, name='login'),
    path('login/', views.login_view, name='my_login'),
    path('signup/', views.signup_view, name='signup_view'),
    path('home/', views.home, name='home'),
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
    path('password_reset/', password_reset_request, name="password_reset_request"),
    path('password_reset/done/', views.password_reset_done_custom, name='password_reset_done_custom'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('custom_password_reset/<str:uidb64>/<str:token>/', views.custom_password_reset, name='custom_password_reset'),
    # path('custom_password_reset_confirm/<uidb64>/<token>/', views.custom_password_reset_confirm, name='custom_password_reset_confirm'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('logout/', views.logout_view, name='logout'),
    path("profile_info/", views.my_profile, name="my_profile"),
]