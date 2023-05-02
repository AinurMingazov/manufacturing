from django.shortcuts import render, get_object_or_404
from itertools import chain
from django.views.generic import ListView, DetailView

from cost.counter_manuf_plan_service import _get_manuf_plan_resources
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


def plan_list(
    request,
):
    """Функция показывает список планов производства"""
    mp = ManufacturingPlan.objects.all()
    return render(request, "cost/plan_list.html", {"mp": mp})


def material_detail(request, id):
    """Функция отображает информацию о применении материала."""
    material = get_object_or_404(Material, id=id)
    return render(
        request,
        "cost/material_detail.html",
        {
            "material": material,
            "detail_materials": DetailMaterial.objects.filter(material=material),
            "assembly_materials": AssemblyMaterial.objects.filter(material=material),
            "product_materials": ProductMaterial.objects.filter(material=material),
        },
    )


def detail_detail(request, id):
    """Функция отображает подробную информацию о детали."""
    detail = get_object_or_404(Detail, id=id)
    return render(
        request,
        "cost/detail_detail.html",
        {
            "detail": detail,
            "detail_labors": DetailLabor.objects.filter(detail=detail),
            "detail_materials": DetailMaterial.objects.filter(detail=detail),
        },
    )


def assembly_detail(request, id):
    """Функция отображает подробную информацию о сборочной единице."""
    assembly = get_object_or_404(Assembly, id=id)
    return render(
        request,
        "cost/assembly_detail.html",
        {
            "assembly": assembly,
            "assemblydetails": AssemblyDetail.objects.filter(assembly=assembly),
            "assemblylabor": AssemblyLabor.objects.filter(assembly=assembly),
            "assemblymaterials": AssemblyMaterial.objects.filter(assembly=assembly),
            "assemblystandarddetail": AssemblyStandardDetail.objects.filter(
                assembly=assembly
            ),
        },
    )


def product_detail(request, id):
    """Функция отображает подробную информацию об изделии."""
    product = get_object_or_404(Product, id=id)
    return render(
        request,
        "cost/product_detail.html",
        {
            "product": product,
            "productdetails": ProductDetail.objects.filter(product=product),
            "productassemblies": ProductAssembly.objects.filter(product=product),
            "productlabor": ProductLabor.objects.filter(product=product),
            "productstandarddetail": ProductStandardDetail.objects.filter(
                product=product
            ),
            "productmaterials": ProductMaterial.objects.filter(product=product),
        },
    )


def mp_resources_count(request, slug):
    """Функция отображает все затраты для выполнения плана."""
    return render(request, "cost/mp_resources_count.html", _get_resources_count(slug))


def mp_detail(request, slug):
    """Функция отображает лист выполнения плана"""
    mp = get_object_or_404(ManufacturingPlan, slug=slug)
    if request.method == "POST":
        _get_manuf_plan_resources(slug)
        return render(
            request, "cost/mp_resources_count.html", _get_resources_count(slug)
        )

    else:
        return render(
            request,
            "cost/mp_detail.html",
            {
                "mp": mp,
                "mpproducts": MPProduct.objects.filter(mp=mp),
                "mpassemblies": MPAssembly.objects.filter(mp=mp),
                "mpdetails": MPDetail.objects.filter(mp=mp),
                "mplabor": MPLabor.objects.filter(mp=mp),
            },
        )


def _get_resources_count(slug):
    mp_res = get_object_or_404(MPResources, slug=slug)
    return {
        "mp_res": mp_res,
        "mprm": MPResourcesMaterial.objects.filter(mp_resources=mp_res),
        "mprl": MPResourcesLabor.objects.filter(mp_resources=mp_res),
        "mprsd": MPResourcesStandardDetail.objects.filter(mp_resources=mp_res),
    }
