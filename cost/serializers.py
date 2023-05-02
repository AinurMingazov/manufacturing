from rest_framework import serializers

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


class ManufacturingPlanSerializer(serializers.ModelSerializer):
    """Вывод плана производства"""

    class Meta:
        model = ManufacturingPlan
        fields = ("id", "name", "slug", "products", "assemblies", "details", "labors")


class ProductSerializer(serializers.ModelSerializer):
    """Вывод изделий"""

    class Meta:
        model = Product
        fields = "__all__"


class AssemblySerializer(serializers.ModelSerializer):
    """Вывод сборок"""

    class Meta:
        model = Assembly
        fields = "__all__"


class DetailSerializer(serializers.ModelSerializer):
    """Вывод деталей"""

    class Meta:
        model = Detail
        fields = "__all__"
