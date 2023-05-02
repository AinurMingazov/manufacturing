from django.shortcuts import get_object_or_404
from rest_framework import viewsets, renderers, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from cost.models import (
    Product,
    ProductDetail,
    ProductStandardDetail,
    Detail,
    DetailLabor,
    ProductLabor,
    ProductAssembly,
    Assembly,
    AssemblyDetail,
    AssemblyLabor,
    AssemblyStandardDetail,
    DetailMaterial,
    ProductMaterial,
    ManufacturingPlan,
    MPResources,
    MPResourcesMaterial,
    MPResourcesLabor,
    MPResourcesStandardDetail,
    MPProduct,
    MPAssembly,
    MPLabor,
    MPDetail,
    Material,
    AssemblyMaterial,
)
from cost.serializers import (
    ManufacturingPlanSerializer,
    ProductSerializer,
    AssemblySerializer,
    DetailSerializer,
)


class ManufacturingPlanListViewSet(viewsets.ModelViewSet):
    queryset = ManufacturingPlan.objects.all()
    serializer_class = ManufacturingPlanSerializer


class ManufacturingPlanViewSet(viewsets.ViewSet):
    def list(self, request, slug=None):
        queryset = ManufacturingPlan.objects.filter(slug=slug)
        serializer = ManufacturingPlanSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    def list(self, request, id=None):
        queryset = Product.objects.filter(id=id)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class AssemblyViewSet(viewsets.ViewSet):
    def list(self, request, id=None):
        queryset = Assembly.objects.filter(id=id)
        serializer = AssemblySerializer(queryset, many=True)
        return Response(serializer.data)


class DetailViewSet(viewsets.ViewSet):
    def list(self, request, id=None):
        queryset = Detail.objects.filter(id=id)
        serializer = DetailSerializer(queryset, many=True)
        return Response(serializer.data)


# class MPlanViewSet(viewsets.ViewSet):
#     def list(self, request, slug=None):
#         queryset = ManufacturingPlan.objects.filter(slug=slug)
#         serializer = MPlanListSerializer(queryset, many=True)
#         return Response(serializer.data)
