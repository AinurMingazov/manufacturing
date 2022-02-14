from django.contrib import admin

from cost.models import Detail, Product, StandardDetail, Labor, Assembly
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget


class ProductDetailInlineAdmin(admin.TabularInline):
    model = Product.details.through


class AssemblyDetailInlineAdmin(admin.TabularInline):
    model = Assembly.details.through


class ProductStandardDetailInlineAdmin(admin.TabularInline):
    model = Product.standard_details.through


class AssemblyStandardDetailInlineAdmin(admin.TabularInline):
    model = Assembly.standard_details.through


class ProductLaborInlineAdmin(admin.TabularInline):
    model = Product.labors.through


class AssemblyLaborInlineAdmin(admin.TabularInline):
    model = Assembly.labors.through


class DetailLaborInlineAdmin(admin.TabularInline):
    model = Detail.labors.through


class AssemblyProductInlineAdmin(admin.TabularInline):
    model = Product.assemblies.through


class DetailResource(resources.ModelResource):
    class Meta:
        model = Detail
        fieldsets = [
            (None, {'fields': ['id', 'name', 'material', 'amount', 'unit', ]})
        ]
        prepopulated_fields = {'slug': ('name',), }
        list_filter = ['name', 'slug']
        inlines = (DetailLaborInlineAdmin,)


class DetailAdmin(ImportExportActionModelAdmin):
    resource_class = DetailResource
    list_display = [field.name for field in Detail._meta.fields if field.name != "id"]
    inlines = [DetailLaborInlineAdmin]


admin.site.register(Detail, DetailAdmin)


class LaborResource(resources.ModelResource):
    class Meta:
        model = Labor
        fields = ('id', 'name', 'machine',)
        list_filter = ['name', 'slug']


class LaborAdmin(ImportExportActionModelAdmin):
    resource_class = LaborResource
    list_display = [field.name for field in Labor._meta.fields if field.name != "id"]


admin.site.register(Labor, LaborAdmin)


class StandardDetailResource(resources.ModelResource):
    class Meta:
        model = StandardDetail
        fields = ('id', 'name',)
        list_filter = ['name', ]


class StandardDetailAdmin(ImportExportActionModelAdmin):
    resource_class = StandardDetailResource
    list_display = [field.name for field in StandardDetail._meta.fields if field.name != "id"]


admin.site.register(StandardDetail, StandardDetailAdmin)


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fieldsets = [
            (None, {'fields': ['name', 'slug', 'amount', 'unit']})
        ]
        prepopulated_fields = {'slug': ('name',), }
        list_filter = ['name', 'slug']
        inlines = (ProductDetailInlineAdmin, ProductStandardDetailInlineAdmin, ProductLaborInlineAdmin,
                   AssemblyProductInlineAdmin)


class ProductAdmin(ImportExportActionModelAdmin):
    resource_class = ProductResource
    list_display = [field.name for field in Product._meta.fields if field.name != "id"]
    inlines = (ProductDetailInlineAdmin, ProductStandardDetailInlineAdmin, ProductLaborInlineAdmin,
               AssemblyProductInlineAdmin)


admin.site.register(Product, ProductAdmin)


class AssemblyResource(resources.ModelResource):
    class Meta:
        model = Assembly
        fieldsets = [
            (None, {'fields': ['name', 'slug', ]})
        ]
        prepopulated_fields = {'slug': ('name',), }
        list_filter = ['name', 'slug']
        inlines = (AssemblyLaborInlineAdmin, AssemblyStandardDetailInlineAdmin, AssemblyDetailInlineAdmin)


class AssemblyAdmin(ImportExportActionModelAdmin):
    resource_class = AssemblyResource
    list_display = [field.name for field in Assembly._meta.fields if field.name != "id"]
    inlines = (AssemblyLaborInlineAdmin, AssemblyStandardDetailInlineAdmin, AssemblyDetailInlineAdmin)


admin.site.register(Assembly, AssemblyAdmin)
