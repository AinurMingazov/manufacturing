from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("cost.urls")),
    path("apiv1/", include("apiv1.urls")),
]
