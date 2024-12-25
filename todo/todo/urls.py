from django.contrib import admin
from django.urls import path
from manage.api import api as manage_api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("manage/", manage_api.urls),
]
