from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("home/admin/", include('loginas.urls')),
    path("", include('admin_material.urls')),
    path('home/accounts/', include('django.contrib.auth.urls'))
]
