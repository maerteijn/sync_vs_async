from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from .. import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.async_view, name="async"),
    path("<int:ms>/", views.api, name="async-ms"),
] + staticfiles_urlpatterns()
