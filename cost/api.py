from django.shortcuts import get_object_or_404
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from cost.models import (Assembly, AssemblyDetail, AssemblyLabor,
                         AssemblyMaterial, AssemblyStandardDetail, Detail,
                         DetailLabor, DetailMaterial, ManufacturingPlan,
                         Material, MPAssembly, MPDetail, MPLabor, MPProduct,
                         MPResources, MPResourcesLabor, MPResourcesMaterial,
                         MPResourcesStandardDetail, Product, ProductAssembly,
                         ProductDetail, ProductLabor, ProductMaterial,
                         ProductStandardDetail)
from cost.serializers import (AssemblySerializer, DetailSerializer,
                              ManufacturingPlanSerializer, ProductSerializer)


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
