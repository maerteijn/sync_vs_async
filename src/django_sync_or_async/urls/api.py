from django.urls import path

from .. import views

urlpatterns = [
    path("", views.api, name="api"),
    path("<int:ms>/", views.api, name="api-ms"),
]
