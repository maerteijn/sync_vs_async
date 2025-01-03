from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from .. import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.gevent_view, name="gevent"),
    path("<int:ms>/", views.gevent_view, name="gevent-ms"),
] + staticfiles_urlpatterns()
