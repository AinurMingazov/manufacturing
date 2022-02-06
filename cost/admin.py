from django.contrib import admin

from cost.models import Detail, Product, StandardDetail, LaborCosts
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget


class DetailInlineAdmin(admin.TabularInline):
    model = Product.details.through


class LaborCostsInlineAdmin(admin.TabularInline):
    model = Detail.detail_labor_costs.through


class StandardDetailInlineAdmin(admin.TabularInline):
    model = Product.standard_details.through

# для загрузки талбиц
class DetailResource(resources.ModelResource):

    class Meta:
        model = Detail
        fieldsets = [
            (None, {'fields': ['name', 'slug', 'material', 'amount_material', 'mat_slug']})
        ]
        prepopulated_fields = {'slug': ('name',), 'mat_slug': ('material',), }
        list_filter = ['name', 'slug']
        inlines = (LaborCostsInlineAdmin,)


class DetailAdmin(ImportExportActionModelAdmin):
    resource_class = DetailResource
    list_display = [field.name for field in Detail._meta.fields if field.name != "id"]
    inlines = [LaborCostsInlineAdmin]
admin.site.register(Detail, DetailAdmin)

# @admin.register(Detail)
# class DetailAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None, {'fields': ['name', 'slug', 'material', 'amount_material', 'mat_slug']})
#     ]
#     prepopulated_fields = {'slug': ('name',), 'mat_slug': ('material',), }
#     list_filter = ['name', 'slug']
#     inlines = ('LaborCostsInlineAdmin',)


class LaborCostsResource(resources.ModelResource):

    class Meta:
        model = LaborCosts
        fields = ('id', 'name', 'machine', 'mach_slug', 'slug')
        prepopulated_fields = {'slug': ('name',), 'mach_slug': ('machine',), }
        list_filter = ['name', 'slug']


class ProductAdmin(ImportExportActionModelAdmin):
    resource_class = ProductResource
    list_display = [field.name for field in Product._meta.fields if field.name != "id"]
    inlines = [DetailInlineAdmin, StandardDetailInlineAdmin]
admin.site.register(Product, ProductAdmin)

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None, {'fields': ['name', 'slug',]})
#     ]
#     prepopulated_fields = {'slug': ('name',)}
#     list_filter = ['name', 'slug']
#     inlines = (DetailInlineAdmin, StandardDetailInlineAdmin)

class LaborCostsAdmin(ImportExportActionModelAdmin):
    resource_class = LaborCostsResource
    list_display = [field.name for field in LaborCosts._meta.fields if field.name != "id"]
admin.site.register(LaborCosts, LaborCostsAdmin)

# @admin.register(LaborCosts)
# class LaborCostsAdmin(admin.ModelAdmin):
#     list_display = ['name', 'machine', 'mach_slug', 'slug']
#     prepopulated_fields = {'slug': ('name',), 'mach_slug': ('machine',), }
#     list_filter = ['name', 'slug']


class StandardDetailResource(resources.ModelResource):

    class Meta:
        model = StandardDetail
        fields = ('id', 'name',  'slug')
        prepopulated_fields = {'slug': ('name',), 'mach_slug': ('machine',), }
        list_filter = ['name', 'slug']


class StandardDetailAdmin(ImportExportActionModelAdmin):
    resource_class = StandardDetailResource
    list_display = [field.name for field in StandardDetail._meta.fields if field.name != "id"]
admin.site.register(StandardDetail, StandardDetailAdmin)


# @admin.register(StandardDetail)
# class StandardDetailAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug',]
#     prepopulated_fields = {'slug': ('name',)}
#     list_filter = ['name', 'slug']

class ProductResource(resources.ModelResource):

    class Meta:
        model = Product
        fieldsets = [
            (None, {'fields': ['name', 'slug', ]})
        ]
        prepopulated_fields = {'slug': ('name',), }
        list_filter = ['name', 'slug']
        inlines = (DetailInlineAdmin, StandardDetailInlineAdmin)


class ProductAdmin(ImportExportActionModelAdmin):
    resource_class = ProductResource
    list_display = [field.name for field in Product._meta.fields if field.name != "id"]
    inlines = [DetailInlineAdmin, StandardDetailInlineAdmin]
admin.site.register(Product, ProductAdmin)

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None, {'fields': ['name', 'slug',]})
#     ]
#     prepopulated_fields = {'slug': ('name',)}
#     list_filter = ['name', 'slug']
#     inlines = (DetailInlineAdmin, StandardDetailInlineAdmin)

