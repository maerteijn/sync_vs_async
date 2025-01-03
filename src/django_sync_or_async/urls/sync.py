from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from .. import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.sync_view, name="sync"),
    path("<int:ms>/", views.sync_view, name="sync-ms"),
] + staticfiles_urlpatterns()
