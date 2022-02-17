from django.urls import path
from . import views


urlpatterns = [
    path("", views.product_list, name='product_list'),
    path('product/<slug:product_slug>/', views.product_detail,
         name='product_detail'),
    path('product_count/<slug:product_slug>/', views.product_count,
         name='product_count'),
    path('<slug:assembly_slug>', views.assembly_detail,
         name='assembly_detail'),
    path('detail/<int:id>/', views.detail_detail,
         name='detail_detail'),
    path('write_plan/', views.write_plan,
             name='write_plan'),
]