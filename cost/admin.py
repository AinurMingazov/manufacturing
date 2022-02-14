from django.contrib import admin

from cost.models import Detail, Product, StandardDetail, Labor, Assembly, Material, ProductResources, ManufacturingPlan
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget


class DetailMaterialInlineAdmin(admin.TabularInline):
    model = Detail.materials.through


class DetailLaborInlineAdmin(admin.TabularInline):
    model = Detail.labors.through


class AssemblyMaterialInlineAdmin(admin.TabularInline):
    model = Assembly.materials.through


class AssemblyDetailInlineAdmin(admin.TabularInline):
    model = Assembly.details.through


class AssemblyStandardDetailInlineAdmin(admin.TabularInline):
    model = Assembly.standard_details.through


class AssemblyLaborInlineAdmin(admin.TabularInline):
    model = Assembly.labors.through


class ProductMaterialInlineAdmin(admin.TabularInline):
    model = Product.materials.through


class ProductDetailInlineAdmin(admin.TabularInline):
    model = Product.details.through


class ProductStandardDetailInlineAdmin(admin.TabularInline):
    model = Product.standard_details.through


class ProductLaborInlineAdmin(admin.TabularInline):
    model = Product.labors.through


class ProductAssemblyInlineAdmin(admin.TabularInline):
    model = Product.assemblies.through


class ProductResourcesMaterialInlineAdmin(admin.TabularInline):
    model = ProductResources.materials.through


class ProductResourcesStandardDetailInlineAdmin(admin.TabularInline):
    model = ProductResources.standard_details.through


class ProductResourcesLaborInlineAdmin(admin.TabularInline):
    model = ProductResources.labors.through


class ManufacturingPlanProductResourcesInlineAdmin(admin.TabularInline):
    model = ManufacturingPlan.product_resources.through


class MaterialResource(resources.ModelResource):
    class Meta:
        model = Material
        fields = ('id', 'name', 'unit',)
        list_filter = ['name', ]


class MaterialAdmin(ImportExportActionModelAdmin):
    resource_class = MaterialResource
    list_display = [field.name for field in Material._meta.fields if field.name != "id"]


admin.site.register(Material, MaterialAdmin)


class LaborResource(resources.ModelResource):
    class Meta:
        model = Labor
        fields = ('id', 'name', 'machine',)
        list_filter = ['name', ]


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


class DetailResource(resources.ModelResource):
    class Meta:
        model = Detail
        fieldsets = [
            (None, {'fields': ['id', 'name', ]})
        ]
        list_filter = ['name', ]
        inlines = (DetailLaborInlineAdmin, DetailMaterialInlineAdmin)


class DetailAdmin(ImportExportActionModelAdmin):
    resource_class = DetailResource
    list_display = [field.name for field in Detail._meta.fields if field.name != "id"]
    inlines = (DetailLaborInlineAdmin, DetailMaterialInlineAdmin)


admin.site.register(Detail, DetailAdmin)


class AssemblyResource(resources.ModelResource):
    class Meta:
        model = Assembly
        fieldsets = [
            (None, {'fields': ['name', 'slug', ]})
        ]
        prepopulated_fields = {'slug': ('name',), }
        list_filter = ['name', 'slug']
        inlines = (AssemblyMaterialInlineAdmin, AssemblyLaborInlineAdmin, AssemblyStandardDetailInlineAdmin,
                   AssemblyDetailInlineAdmin)


class AssemblyAdmin(ImportExportActionModelAdmin):
    resource_class = AssemblyResource
    list_display = [field.name for field in Assembly._meta.fields if field.name != "id"]
    inlines = (AssemblyMaterialInlineAdmin, AssemblyLaborInlineAdmin, AssemblyStandardDetailInlineAdmin,
               AssemblyDetailInlineAdmin)


admin.site.register(Assembly, AssemblyAdmin)


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fieldsets = [
            (None, {'fields': ['name', 'slug']})
        ]
        prepopulated_fields = {'slug': ('name',), }
        list_filter = ['name', 'slug']
        inlines = (ProductDetailInlineAdmin, ProductStandardDetailInlineAdmin, ProductLaborInlineAdmin,
                   ProductAssemblyInlineAdmin, ProductMaterialInlineAdmin)


class ProductAdmin(ImportExportActionModelAdmin):
    resource_class = ProductResource
    list_display = [field.name for field in Product._meta.fields if field.name != "id"]
    inlines = (ProductDetailInlineAdmin, ProductStandardDetailInlineAdmin, ProductLaborInlineAdmin,
               ProductAssemblyInlineAdmin, ProductMaterialInlineAdmin)


admin.site.register(Product, ProductAdmin)


class ProductResourcesResource(resources.ModelResource):
    class Meta:
        model = ProductResources
        fieldsets = [
            (None, {'fields': ['name', 'slug']})
        ]
        prepopulated_fields = {'slug': ('name',), }
        list_filter = ['name', 'slug']
        inlines = (ProductResourcesMaterialInlineAdmin, ProductResourcesStandardDetailInlineAdmin,
                   ProductResourcesLaborInlineAdmin)


class ProductResourcesAdmin(ImportExportActionModelAdmin):
    resource_class = ProductResourcesResource
    list_display = [field.name for field in ProductResources._meta.fields if field.name != "id"]
    inlines = (ProductResourcesMaterialInlineAdmin, ProductResourcesStandardDetailInlineAdmin,
               ProductResourcesLaborInlineAdmin)


admin.site.register(ProductResources, ProductResourcesAdmin)


class ManufacturingPlanResource(resources.ModelResource):
    class Meta:
        model = ManufacturingPlan
        fieldsets = [
            (None, {'fields': ['name', ]})
        ]
        list_filter = ['name', ]
        inlines = (ManufacturingPlanProductResourcesInlineAdmin,)


class ManufacturingPlanAdmin(ImportExportActionModelAdmin):
    resource_class = ManufacturingPlanResource
    list_display = [field.name for field in ManufacturingPlan._meta.fields if field.name != "id"]
    inlines = (ManufacturingPlanProductResourcesInlineAdmin,)


admin.site.register(ManufacturingPlan, ManufacturingPlanAdmin)
