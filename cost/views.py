from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View
from cost import models
from cost.counter_manuf_plan_service import _get_manuf_plan_resources
from cost import forms
from cost.services.materials_parcer import parser_material


@staff_member_required
def parser():
    """Функция заполняет или обновляет данные о материалах в БД"""
    parser_material()
    return HttpResponse("Parser worked")


def material_list(request):
    """Функция показывает список материалов"""
    materials = models.Material.objects.all().order_by("price_per_ton")
    return render(request, "cost/material_list.html", {"materials": materials})


def standard_detail_list(request):
    """Функция показывает список стандартных изделий"""
    standard_details = models.StandardDetail.objects.all().order_by("name")
    return render(
        request,
        "cost/standard_detail_list.html",
        {"standard_details": standard_details},
    )


def detail_list(request):
    """Функция показывает список деталей"""
    details = models.Detail.objects.all().order_by("name")
    return render(request, "cost/detail_list.html", {"details": details})


def assembly_list(request):
    """Функция показывает список сборочных единиц"""
    assemblies = models.Assembly.objects.all().order_by("name")
    return render(request, "cost/assembly_list.html", {"assemblies": assemblies})


def product_list(request):
    """Функция показывает список изделий"""
    products = models.Product.objects.all().order_by("name")
    return render(request, "cost/product_list.html", {"products": products})


def plan_list(request):
    """Функция показывает список планов производства"""
    mp = models.ManufacturingPlan.objects.all()
    return render(request, "cost/plan_list.html", {"mp": mp})


class MaterialDetail(View):
    """Отображает информацию о материале и в составе каких элементов оно участвует"""
    def get(self, request, slug):
        material = get_object_or_404(models.Material, slug=slug)
        return render(request,
                      "cost/material_detail.html",
                      {"material": material,
                       "detail_materials": models.DetailMaterial.objects.filter(material=material),
                       "assembly_materials": models.AssemblyMaterial.objects.filter(material=material),
                       "product_materials": models.ProductMaterial.objects.filter(material=material)})


class MaterialCreate(View):
    def get(self, request):
        form = forms.MaterialForm()
        return render(request, "cost/forms/material_create.html", context={"form": form})

    def post(self, request):
        bound_form = forms.MaterialForm(request.POST)
        if bound_form.is_valid():
            new_material = bound_form.save()
            return redirect(new_material)
        return render(request, "cost/forms/material_create.html", context={"form": bound_form})


def standard_detail(request, slug):
    """Функция отображает информацию о применении материала."""
    standard_detail = get_object_or_404(models.StandardDetail, slug=slug)
    return render(
        request,
        "cost/material_detail.html",
        {
            "standard_detail": standard_detail,
            "detail_materials": models.DetailMaterial.objects.filter(
                standard_detail=standard_detail
            ),
            "assembly_materials": models.AssemblyMaterial.objects.filter(
                material=standard_detail
            ),
            "product_materials": models.ProductMaterial.objects.filter(
                material=standard_detail
            ),
        },
    )


def detail_detail(request, slug):
    """Функция отображает подробную информацию о детали."""
    detail = get_object_or_404(models.Detail, slug=slug)
    return render(
        request,
        "cost/detail_detail.html",
        {
            "detail": detail,
            "detail_labors": models.DetailLabor.objects.filter(detail=detail),
            "detail_materials": models.DetailMaterial.objects.filter(detail=detail),
        },
    )


def assembly_detail(request, slug):
    """Функция отображает подробную информацию о сборочной единице."""
    assembly = get_object_or_404(models.Assembly, slug=slug)
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


def product_detail(request, slug):
    """Функция отображает подробную информацию об изделии."""
    product = get_object_or_404(models.Product, slug=slug)
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
