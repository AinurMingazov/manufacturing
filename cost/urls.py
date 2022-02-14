from django.urls import path
from . import views


urlpatterns = [
    path("", views.product_list, name='product_list'),
    path('<slug:product_slug>/', views.product_detail,
         name='product_detail'),
    path('requirements/<slug:product_slug>/', views.product_requirements,
         name='product_requirements'),
    path('<slug:assembly_slug>', views.assembly_detail,
         name='assembly_detail'),
    path('detail/<int:id>/', views.detail_detail,
         name='detail_detail'),
]