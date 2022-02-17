from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from itertools import chain
from django.views.generic import ListView, DetailView

from cost.forms import ManufacturingPlanForm, ManufacturingPlanProductResourcesForm
from cost.models import Product, ProductDetail, ProductStandardDetail, Detail, DetailLabor, ProductLabor, \
    ProductAssembly, Assembly, AssemblyDetail, AssemblyLabor, AssemblyStandardDetail, DetailMaterial, ProductMaterial, \
    ProductResourcesMaterial, ProductResources, ProductResourcesLabor, ProductResourcesStandardDetail


def product_list(request,):
    """Функция показывает список изделий"""
    product = Product.objects.all()
    return render(request,
                  'cost/product_list.html',
                  {'product': product,
                   })


def detail_detail(request, id):
    """Функция отображает подробную информацию о детали."""
    detail = get_object_or_404(Detail, id=id)
    detail_labors = DetailLabor.objects.filter(detail=detail)
    detail_materials = DetailMaterial.objects.filter(detail=detail)
    return render(request,
                  'cost/detail_detail.html',
                  {'detail': detail,
                   'detail_labors': detail_labors,
                   'detail_materials': detail_materials
                   })


def assembly_detail(request, assembly_slug):
    """Функция отображает подробную информацию о сборочной единице."""
    assembly = get_object_or_404(Assembly, slug=assembly_slug)
    assemblydetails = AssemblyDetail.objects.filter(assembly=assembly)
    assemblylabor = AssemblyLabor.objects.filter(assembly=assembly)
    assemblystandarddetail = AssemblyStandardDetail.objects.filter(assembly=assembly)
    print(assemblylabor)
    return render(request,
                  'cost/assembly_detail.html',
                  {'assembly': assembly,
                   'assemblydetails': assemblydetails,
                   'assemblylabor': assemblylabor,
                   'assemblystandarddetail': assemblystandarddetail
                   })

def product_detail(request, product_slug):
    """Функция отображает все затраты для изготовления продукта."""
    product = get_object_or_404(Product, slug=product_slug)

    if request.method == "POST":
        dict_material = dict()
        dict_labor = dict()
        dict_stand = dict()

        for assembly in ProductAssembly.objects.filter(product=product):
            # перебираем узлы в изделии
            for detail in assembly.assembly.details.all():
                # перебираем детали в узле
                for assemblydetail in AssemblyDetail.objects.filter(detail_id=detail.id).filter(assembly_id=assembly.id):
                    # перебираем модель отношения деталей в узле, для возможности обратиться к количеству деталей в узле
                    for det in DetailMaterial.objects.filter(detail_id=detail.id):
                        # перебираем модель отношение материалов в деталях, для возможности обратиться к количеству
                        # материалов в детали
                        count = det.amount * assemblydetail.amount * assembly.amount
                        # соберем словарь ключ=(id материала) значение=(количество)
                        temp_dict = dict.fromkeys([det.material.id], count)
                        try:
                            dict_material[det.material.id] += temp_dict[det.material.id]
                        except KeyError:
                            dict_material[det.material.id] = temp_dict[det.material.id]
                    for assemblydetlab in DetailLabor.objects.filter(detail_id=detail.id):
                        # перебираем трудозатраты деталей узла
                        count = assemblydetlab.time * assemblydetail.amount * assembly.amount
                        # print(detail.name + ' - ' + str(assemblydetlab.labor.id) + ' - ' + assemblydetlab.labor.name
                        #       + ' - ' + assemblydetlab.labor.machine + ' - ' + str(assemblydetlab.time)
                        #       + ' * ' + str(assemblydetail.amount) + ' * ' + str(assembly.amount) + ' = ' +
                        #       str(count))
                        # собираем все трудозатраты в словарь, чтобы объединить работы выполняемые на одном станке
                        temp_dict = dict.fromkeys([assemblydetlab.labor.id], count)
                        try:
                            dict_labor[assemblydetlab.labor.id] += temp_dict[assemblydetlab.labor.id]
                        except KeyError:
                            dict_labor[assemblydetlab.labor.id] = temp_dict[assemblydetlab.labor.id]
            for standetail in assembly.assembly.standard_details.all():
            # перебираем стандартные изделия в узле
                for assemstanddet in AssemblyStandardDetail.objects.filter(standard_detail_id=standetail.id)\
                        .filter(assembly_id=assembly.id):
                    # перебираем модель отношения стандартных изделий в узле, для возможности обратиться
                    # к количеству стандартных изделий в узле
                    count = assemstanddet.amount * assembly.amount
                    # print(assemstanddet.standard_detail.name + ' - ' + str(assemstanddet.amount)
                    #       + ' * ' + str(assembly.amount) + ' = ' + str(count))
                    temp_dict = dict.fromkeys([assemstanddet.standard_detail.id], count)
                    try:
                        dict_stand[assemstanddet.standard_detail.id] += temp_dict[assemstanddet.standard_detail.id]
                    except KeyError:
                        dict_stand[assemstanddet.standard_detail.id] = temp_dict[assemstanddet.standard_detail.id]
        for productdetail in ProductDetail.objects.filter(product=product):
            # перебираем детали в изделии
            # print(productdetail.detail.name + ' - ' + str(productdetail.amount))
            for detmat in DetailMaterial.objects.filter(detail_id=productdetail.detail.id):
                # перебираем модель отношение материалов в деталях, для возможности обратиться к количеству
                # материалов в детали
                count = detmat.amount * productdetail.amount
                # print(productdetail.detail.name + ' - ' + detmat.material.name + ' - ' + str(productdetail.amount) +
                #       ' * ' + str(detmat.amount) + ' = ' + str(count))
                temp_dict = dict.fromkeys([detmat.material.id], count)
                try:
                    dict_material[detmat.material.id] += temp_dict[detmat.material.id]
                except KeyError:
                    dict_material[detmat.material.id] = temp_dict[detmat.material.id]
            for detlab in DetailLabor.objects.filter(detail_id=productdetail.detail.id):
                count = detlab.time * productdetail.amount
                # print(str(detlab.labor.id) + ' - ' + detlab.labor.name + ' - ' + detlab.labor.machine
                #       + ' - ' + str(detlab.time) + ' - ' + str(count))
                temp_dict = dict.fromkeys([detlab.labor.id], count)
                try:
                    dict_labor[detlab.labor.id] += temp_dict[detlab.labor.id]
                except KeyError:
                    dict_labor[detlab.labor.id] = temp_dict[detlab.labor.id]
        for prodmat in ProductMaterial.objects.filter(product=product):
            # print(prodmat.material.name + ' - ' + str(prodmat.amount))
            temp_dict = dict.fromkeys([prodmat.material.id], prodmat.amount)
            try:
                dict_material[prodmat.material.id] += temp_dict[prodmat.material.id]
            except KeyError:
                dict_material[prodmat.material.id] = temp_dict[prodmat.material.id]

        for prodlab in ProductLabor.objects.filter(product=product):
            # print(prodmat.material.name + ' - ' + str(prodmat.amount))
            temp_dict = dict.fromkeys([prodlab.labor.id], prodlab.time)
            try:
                dict_labor[prodlab.labor.id] += temp_dict[prodlab.labor.id]
            except KeyError:
                dict_labor[prodlab.labor.id] = temp_dict[prodlab.labor.id]
        for standdet in ProductStandardDetail.objects.filter(product=product):
            # print(standdet.standard_detail.name + ' - ' + str(standdet.amount))
            temp_dict = dict.fromkeys([standdet.standard_detail.id], standdet.amount)
            try:
                dict_stand[standdet.standard_detail.id] += temp_dict[standdet.standard_detail.id]
            except KeyError:
                dict_stand[standdet.standard_detail.id] = temp_dict[standdet.standard_detail.id]

        try:
            pr = ProductResources.objects.create(name=product.name, slug=product.slug)
            for key, value in dict_material.items():
                ProductResourcesMaterial.objects.create(
                    product_resources_id=pr.id, material_id=key, amount=value)
            for key, value in dict_labor.items():
                ProductResourcesLabor.objects.create(
                    product_resources_id=pr.id, labor_id=key, time=value)
            for key, value in dict_stand.items():
                ProductResourcesStandardDetail.objects.create(
                    product_resources_id=pr.id, standard_detail_id=key, amount=value)
        except IntegrityError:
                product_count(request, product_slug)

        prodres = get_object_or_404(ProductResources, slug=product_slug)
        prm = ProductResourcesMaterial.objects.filter(product_resources=prodres)
        prl = ProductResourcesLabor.objects.filter(product_resources=prodres)
        prsd = ProductResourcesStandardDetail.objects.filter(product_resources=prodres)

        return render(request,
                      'cost/product_count.html',
                      {'prodres': prodres,
                       'prm': prm,
                       'prl': prl,
                       'prsd': prsd,

                       })

    else:
        productdetails = ProductDetail.objects.filter(product=product)
        productassemblies = ProductAssembly.objects.filter(product=product)
        productlabor = ProductLabor.objects.filter(product=product)
        productstandarddetail = ProductStandardDetail.objects.filter(product=product)

        return render(request,
                      'cost/product_detail.html',
                      {'product': product,
                       'productdetails': productdetails,
                       'productassemblies': productassemblies,
                       'productlabor': productlabor,
                       'productstandarddetail': productstandarddetail,

                       })


def product_count(request, product_slug):
    """Функция отображает все затраты для изготовления продукта."""
    prodres = get_object_or_404(ProductResources, slug=product_slug)
    prm = ProductResourcesMaterial.objects.filter(product_resources=prodres)
    prl = ProductResourcesLabor.objects.filter(product_resources=prodres)
    prsd = ProductResourcesStandardDetail.objects.filter(product_resources=prodres)

    return render(request,
                  'cost/product_count.html',
                  {'prodres': prodres,
                   'prm': prm,
                   'prl': prl,
                   'prsd': prsd,

                   })


def write_plan(request,):
    prodres = ProductResources.objects.all()

    if request.method == "POST":
        mpform = ManufacturingPlanForm(request.POST)
        mpprform = ManufacturingPlanProductResourcesForm(request.POST)

    else:
        mpform = ManufacturingPlanForm()
        mpprform = ManufacturingPlanProductResourcesForm()

    return render(request,
                  'cost/write_plan.html',
                  {'prodres': prodres, 'mpform': mpform, 'mpprform': mpprform,
                   })