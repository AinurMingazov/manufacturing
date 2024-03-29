from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import api, views

urlpatterns = [
    path("", views.plan_list, name="plan_list"),
    path("materials/", views.material_list, name="material_list"),
    path("standard_details/", views.standard_detail_list, name="standard_detail_list"),
    path("details/", views.detail_list, name="detail_list"),
    path("assemblies/", views.assembly_list, name="assembly_list"),
    path("products/", views.product_list, name="product_list"),

    path("parser/", views.parser, name="parser"),
    path("material/create", views.MaterialCreate.as_view(), name="material_create"),

    path("material/<slug:slug>/", views.MaterialDetail.as_view(), name="material_detail"),
    path("standard_detail/<slug:slug>/", views.standard_detail, name="standard_detail_detail"),
    path("detail/<slug:slug>/", views.detail_detail, name="detail_detail"),
    path("assembly/<slug:slug>/", views.assembly_detail, name="assembly_detail"),
    path("plan/<slug:slug>/", views.mp_detail, name="mp_detail"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("mp_resources_count/<slug:slug>/", views.mp_resources_count, name="mp_resources_count"),
]

urlpatterns_api = format_suffix_patterns(
    [
        path("api/plan/", api.ManufacturingPlanListViewSet.as_view({"get": "list"})),
        path(
            "api/plan/<slug:slug>/",
            api.ManufacturingPlanViewSet.as_view({"get": "list"}),
        ),
        path("api/product/<int:id>/", api.ProductViewSet.as_view({"get": "list"})),
        path("api/assembly/<int:id>/", api.AssemblyViewSet.as_view({"get": "list"})),
        path("api/detail/<int:id>/", api.DetailViewSet.as_view({"get": "list"})),
    ]
)

urlpatterns += urlpatterns_api
