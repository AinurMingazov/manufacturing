from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views, api


urlpatterns = [
    path("", views.plan_list, name="plan_list"),
    path("plan/<slug:slug>/", views.mp_detail, name="mp_detail"),
    path("product/<int:id>/", views.product_detail, name="product_detail"),
    path("assembly/<int:id>/", views.assembly_detail, name="assembly_detail"),
    path("detail/<int:id>/", views.detail_detail, name="detail_detail"),
    path("material/<int:id>/", views.material_detail, name="material_detail"),
    path(
        "mp_resources_count/<slug:slug>/",
        views.mp_resources_count,
        name="mp_resources_count",
    ),
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
