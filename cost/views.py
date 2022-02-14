from django.shortcuts import render, get_object_or_404
from itertools import chain
# Create your views here.
from django.views.generic import ListView, DetailView

from cost.models import Product, ProductDetail, ProductStandardDetail, Detail, DetailLabor, ProductLabor, \
    ProductAssembly, Assembly, AssemblyDetail, AssemblyLabor, AssemblyStandardDetail, DetailMaterial


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
    """Функция отображает подробную информацию о продукте."""
    product = get_object_or_404(Product, slug=product_slug)
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
                   'productstandarddetail': productstandarddetail
                   })


def product_requirements(request, product_slug):
    """Функция отображает все затраты для изготовления продукта."""
    product = get_object_or_404(Product, slug=product_slug)
    productassemblies = ProductAssembly.objects.filter(product=product)
    assembly_detail_material_dict = dict()
    for assembly in productassemblies.all():
        for detail in assembly.assembly.details.all():
            assemblydetails = AssemblyDetail.objects.filter(detail_id=detail.id)
            for assemblydetail in assemblydetails.all():
                pass
            count = detail.amount * assemblydetail.amount_details * assembly.amount_assemblies
            temp_dict = dict.fromkeys([detail.id], count)
            try:
                assembly_detail_material_dict[detail.id] += temp_dict[detail.id]
            except KeyError:
                assembly_detail_material_dict[detail.id] = temp_dict[detail.id]

    productdetails = ProductDetail.objects.filter(product=product)
    detail_material_dict = dict()
    for detail in productdetails.all():
        count = detail.detail.amount * detail.amount_details
        temp_dict = dict.fromkeys([detail.id], count)
        print(temp_dict)
        try:
            detail_material_dict[detail.id] += temp_dict[detail.id]
        except KeyError:
            detail_material_dict[detail.id] = temp_dict[detail.id]



    productlabor = ProductLabor.objects.filter(product=product)
    productstandarddetail = ProductStandardDetail.objects.filter(product=product)





    print(detail_material_dict)
    materials = Detail.objects.filter(id__in=detail_material_dict.keys())
    for material, val in zip(materials, detail_material_dict.values()):
        print(material.material + ' - ' + str(val))

    return render(request,
                  'cost/product_requirements.html',
                  {'product': product,
                   'productdetails': productdetails,
                   'productassemblies': productassemblies,
                   'productlabor': productlabor,
                   'productstandarddetail': productstandarddetail,

                   })


#
# class ProductsView(ListView):
#     """Список изделий"""
#     model = Product
#     queryset = Product.objects.all()


# class ProductDetailView(DetailView):
#     """Полное описание изделия"""
#     model = Product
#     slug_field = "slug"
#     print(model)
#     print("model_id")
#     print(model.details)
# print(model.self.request.query_params.get('id'))
# product = Product.objects.filter(slug="slug")
# print(product)
# proid = product.id
# details = ProductDetail.objects.filter(id=proid)
#

# def get_productdetails(self, request):
#     product_id = self.request.query_params.get('slug')
#     productdetails = ProductDetail.objects.filter(id=product_id)
#     return print(productdetails)
#     product = Product.objects.filter(id=product_id)
#     print(product)


# def productdetails_detail(request, product_slug):
#     """Функция отображает подробную информацию о продукте."""
#     product = get_object_or_404(Product, slug=product_slug)
#     productdetails = ProductDetail.objects.filter(product=product)

    # productstandarddetails = ProductStandardDetail.objects.filter(product=product)
    # details = productdetails.filter(detail__in=detail.detail)


# Следующая конструкция позволяет объединить трудозатраты по станкам
#     detaillaborcosts = []
#     for detail in productdetails.all():  # Собираем в список все трудозатраты всех деталей через изделия
#         detaillaborcosts=list(chain(detaillaborcosts, DetailLabor.objects.filter(detail=detail.detail)))
#     labor_machine_list = []
#     for labor in detaillaborcosts:  # Собираем в словарь все станки - ключ слаг станка : значение = 0
#         labor_machine_list.append(labor.labor.mach_slug)
#     labor_machine = dict.fromkeys(labor_machine_list, 0)
#     for labor in detaillaborcosts:  # Создаем временный словарь и добавляем его значения в основной
#         temp_dict = dict.fromkeys([labor.labor.mach_slug], labor.time_details)
#         try:
#             labor_machine[labor.labor.mach_slug] += temp_dict[labor.labor.mach_slug]
#         except KeyError:  # Если ключа еще нет - создаем
#             labor_machine[labor.labor.mach_slug] = temp_dict[labor.labor.mach_slug]

    # Следующая конструкция позволяет объединить одинаковые стандартные изделия
    # productstandarddetails_list = []
    # for detail in productstandarddetails:
    #     productstandarddetails_list.append(detail.standard_detail.slug)
    # standard_details = dict.fromkeys(productstandarddetails_list, 0)
    # for detail in productstandarddetails:
    #     temp_dict = dict.fromkeys([detail.standard_detail.slug], detail.amount_standard_detail)
    #     try:
    #         standard_details[detail.standard_detail.slug] += temp_dict[detail.standard_detail.slug]
    #     except KeyError:
    #         standard_details[detail.standard_detail.slug] = temp_dict[detail.standard_detail.slug]

        # Следующая конструкция позволяет объединить одинаковые материал
        # materialdetails_list = []
        # for detail in productdetails:
        #     materialdetails_list.append(detail.detail.mat_slug)
        # details = dict.fromkeys(materialdetails_list, 0)
        # for detail in productdetails:
        #     temp_dict = dict.fromkeys([detail.detail.mat_slug], detail.detail.amount_material)
        #     try:
        #         details[detail.detail.mat_slug] += temp_dict[detail.detail.mat_slug]
        #     except KeyError:
        #         details[detail.detail.mat_slug] = temp_dict[detail.detail.mat_slug]

    # return render(request,
    #               'cost/product_detail.html',
    #               {'product': product,
    #                'productdetails': productdetails,
    #                'details': details,
    #                'standard_details': standard_details,
    #                'labor_machine': labor_machine
    #                })
