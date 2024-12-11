from django.contrib import admin
from django.urls import re_path, include

from django.urls import path, include
from rest_framework.routers import DefaultRouter


urlpatterns = [
    # path("", include(router.urls)),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
