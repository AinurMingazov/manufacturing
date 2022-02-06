from django.shortcuts import render, get_object_or_404
from itertools import chain
# Create your views here.
from django.views.generic import ListView, DetailView

from cost.models import Product, ProductDetail, ProductStandardDetail, Detail, DetailLaborCosts


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


def product_list(request,):
    """Функция показываем все инструменты по умолчанию,
    позволяет настроить фильтр по категориям и/или по владельцам."""
    product = Product.objects.all()
    return render(request,
                  'cost/product_list.html',
                  {'product': product,
                   })


def productdetails_detail(request, product_slug):
    """Функция отображает подробную информацию о продукте."""
    product = get_object_or_404(Product, slug=product_slug)
    detaillaborcosts = []
    productdetails = ProductDetail.objects.filter(product=product)
    productstandarddetails = ProductStandardDetail.objects.filter(product=product)
    for detail in productdetails.all():
        detaillaborcosts=list(chain(detaillaborcosts, DetailLaborCosts.objects.filter(detail=detail.detail)))
        print(detaillaborcosts)
        labor_machine_list = []
        labor_machine = {}
        for labor in detaillaborcosts:
            labor_machine_list.append(labor.labor.machine)
            print(set(labor_machine_list))
        for labor in detaillaborcosts:

            if labor.labor.machine in labor_machine_list:
                labor_machine[labor.labor.machine] += labor.time_details

            labor_machine_list.append(labor.labor.machine)
            print(labor_machine)
    # print(labor.labor.machine)
    # if labor.labor.machine in labor_machine_list:
    #     labor.time_details += labor.time_details
    #     detaillaborcosts.remove(labor)

    return render(request,
                  'cost/product_detail.html',
                  {'product': product,
                   'productdetails': productdetails,
                   'productstandarddetails': productstandarddetails,
                   'detaillaborcosts': detaillaborcosts
                   })

