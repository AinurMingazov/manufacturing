from django.contrib import admin

from material_consumption.models import Detail,  Product, ProductDetail


class DetailInlineAdmin(admin.TabularInline):
    model = Product.details.through


@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'material', 'amount_material', 'unit', 'weight', 'price']


# @admin.register(StandardDetail)
# class StandardDetailAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'slug', 'amount_material', 'unit', 'price', 'through_fields']
#     through_fields = ('amount', 'product', 'standart_detail')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields' : ['name', 'slug', 'amount', 'unit', 'price']})
    ]
    inlines = (DetailInlineAdmin,)


# @admin.register(ProductDetail)
# class ProductDetailAdmin(admin.ModelAdmin):
#     list_display = ['id', 'product', 'detail', 'amount']
#
#
# @admin.register(ProductStandardDetail)
# class ProductStandardDetailAdmin(admin.ModelAdmin):
#     list_display = ['id', 'product', 'standart_detail', 'amount']

