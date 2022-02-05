from django.urls import path
from . import views


urlpatterns = [
    path("", views.product_list),
    # path("<slug:slug>/", views.ProductDetailView.as_view(),  name="product_detail"),
    path('<slug:product_slug>/', views.productdetails_detail,
         name='product_detail'),
]