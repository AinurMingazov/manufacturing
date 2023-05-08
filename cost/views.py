from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from cost.counter_manuf_plan_service import _get_manuf_plan_resources
from cost import models

from cost.services.materials_parcer import parser_material


@staff_member_required
def parser(
    request,
):
    """Функция заполняет или обновляет данные о материалах в БД"""
    parser_material()
    return HttpResponse("Parser worked")


def plan_list(
    request,
):
    """Функция показывает список планов производства"""
    mp = models.ManufacturingPlan.objects.all()
    return render(request, "cost/plan_list.html", {"mp": mp})


def material_detail(request, id):
    """Функция отображает информацию о применении материала."""
    material = get_object_or_404(models.Material, id=id)
    return render(
        request,
        "cost/material_detail.html",
        {
            "material": material,
            "detail_materials": models.DetailMaterial.objects.filter(material=material),
            "assembly_materials": models.AssemblyMaterial.objects.filter(
                material=material
            ),
            "product_materials": models.ProductMaterial.objects.filter(
                material=material
            ),
        },
    )


def detail_detail(request, id):
    """Функция отображает подробную информацию о детали."""
    detail = get_object_or_404(models.Detail, id=id)
    return render(
        request,
        "cost/detail_detail.html",
        {
            "detail": detail,
            "detail_labors": models.DetailLabor.objects.filter(detail=detail),
            "detail_materials": models.DetailMaterial.objects.filter(detail=detail),
        },
    )


def assembly_detail(request, id):
    """Функция отображает подробную информацию о сборочной единице."""
    assembly = get_object_or_404(models.Assembly, id=id)
    return render(
        request,
        "cost/assembly_detail.html",
        {
            "assembly": assembly,
            "assemblydetails": models.AssemblyDetail.objects.filter(assembly=assembly),
            "assemblylabor": models.AssemblyLabor.objects.filter(assembly=assembly),
            "assemblymaterials": models.AssemblyMaterial.objects.filter(
                assembly=assembly
            ),
            "assemblystandarddetail": models.AssemblyStandardDetail.objects.filter(
                assembly=assembly
            ),
        },
    )


def product_detail(request, id):
    """Функция отображает подробную информацию об изделии."""
    product = get_object_or_404(models.Product, id=id)
    return render(
        request,
        "cost/product_detail.html",
        {
            "product": product,
            "productdetails": models.ProductDetail.objects.filter(product=product),
            "productassemblies": models.ProductAssembly.objects.filter(product=product),
            "productlabor": models.ProductLabor.objects.filter(product=product),
            "productstandarddetail": models.ProductStandardDetail.objects.filter(
                product=product
            ),
            "productmaterials": models.ProductMaterial.objects.filter(product=product),
        },
    )


def mp_resources_count(request, slug):
    """Функция отображает все затраты для выполнения плана."""
    return render(request, "cost/mp_resources_count.html", _get_resources_count(slug))


def mp_detail(request, slug):
    """Функция отображает лист выполнения плана"""
    mp = get_object_or_404(models.ManufacturingPlan, slug=slug)
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
                "mpproducts": models.MPProduct.objects.filter(mp=mp),
                "mpassemblies": models.MPAssembly.objects.filter(mp=mp),
                "mpdetails": models.MPDetail.objects.filter(mp=mp),
                "mplabor": models.MPLabor.objects.filter(mp=mp),
            },
        )


def _get_resources_count(slug):
    mp_res = get_object_or_404(models.MPResources, slug=slug)
    return {
        "mp_res": mp_res,
        "mprm": models.MPResourcesMaterial.objects.filter(mp_resources=mp_res),
        "mprl": models.MPResourcesLabor.objects.filter(mp_resources=mp_res),
        "mprsd": models.MPResourcesStandardDetail.objects.filter(mp_resources=mp_res),
    }
