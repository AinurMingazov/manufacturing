from django.contrib import admin

from cost.models import Detail, Product, StandardDetail, Labor, Assembly
# from import_export.admin import ImportExportActionModelAdmin
# from import_export import resources, fields
# from import_export.widgets import ForeignKeyWidget


# class DetailInlineAdmin(admin.TabularInline):
#     def change_view(self, request, model):
#         model = self.model
#         obj = self.get_object(request, model)
#
#         if obj.model == 'Product':
#             self.inlines = Product.details.through
#         elif obj.model == 'Assembly':
#             self.inlines = Assembly.details.through
#
#         return super(Detail, self).change_view(request, model)
#
#
# class LaborInlineAdmin(admin.TabularInline):
#     def change_view(self, request, model):
#         model = self.model
#         obj = self.get_object(request, model)
#         if obj.model == 'Product':
#             self.inlines = Product.product_labors.through
#         elif obj.model == 'Assembly':
#             self.inlines = Assembly.assembly_labors.through
#         elif obj.model == 'Assembly':
#             self.inlines = Detail.detail_labors.through
#
#         return super(Labor, self).change_view(request, model)
#
#
# class StandardDetailInlineAdmin(admin.TabularInline):
#     def change_view(self, request, model):
#         model = self.model
#         obj = self.get_object(request, model)
#
#         if obj.model == 'Product':
#             self.inlines = Product.standard_details.through
#         elif obj.model == 'Assembly':
#             self.inlines = Assembly.standard_details.through
#         return super(StandardDetail, self).change_view(request, model)
#
#
# class DetailResource(resources.ModelResource):
#     class Meta:
#         model = Detail
#         fieldsets = [
#             (None, {'fields': ['id', 'name', 'material', 'amount_material', ]})
#         ]
#         # prepopulated_fields = {'slug': ('name',), 'mat_slug': ('material',), }
#         list_filter = ['name', 'slug']
#         inlines = (LaborInlineAdmin,)
#
#
# class DetailAdmin(ImportExportActionModelAdmin):
#     resource_class = DetailResource
#     list_display = [field.name for field in Detail._meta.fields if field.name != "id"]
#     inlines = [LaborInlineAdmin]
#
#
# admin.site.register(Detail, DetailAdmin)
#
#
# class LaborResource(resources.ModelResource):
#     class Meta:
#         model = Labor
#         fields = ('id', 'name', 'machine',)
#         # prepopulated_fields = {'slug': ('name',), 'mach_slug': ('machine',), }
#         list_filter = ['name', 'slug']
#
#
# class LaborAdmin(ImportExportActionModelAdmin):
#     resource_class = LaborResource
#     list_display = [field.name for field in Labor._meta.fields if field.name != "id"]
#
#
# admin.site.register(Labor, LaborAdmin)
#
#
# class StandardDetailResource(resources.ModelResource):
#     class Meta:
#         model = StandardDetail
#         fields = ('id', 'name',)
#         # prepopulated_fields = {'slug': ('name',), 'mach_slug': ('machine',), }
#         list_filter = ['name', ]
#
#
# class StandardDetailAdmin(ImportExportActionModelAdmin):
#     resource_class = StandardDetailResource
#     list_display = [field.name for field in StandardDetail._meta.fields if field.name != "id"]
#
#
# admin.site.register(StandardDetail, StandardDetailAdmin)
#
#
# class ProductResource(resources.ModelResource):
#     class Meta:
#         model = Product
#         fieldsets = [
#             (None, {'fields': ['name', 'slug', ]})
#         ]
#         prepopulated_fields = {'slug': ('name',), }
#         list_filter = ['name', 'slug']
#         inlines = (DetailInlineAdmin, StandardDetailInlineAdmin, LaborInlineAdmin)
#
#
# class ProductAdmin(ImportExportActionModelAdmin):
#     resource_class = ProductResource
#     list_display = [field.name for field in Product._meta.fields if field.name != "id"]
#     inlines = [DetailInlineAdmin, StandardDetailInlineAdmin, LaborInlineAdmin]
#
#
# admin.site.register(Product, ProductAdmin)
#
#
# class AssemblyResource(resources.ModelResource):
#     class Meta:
#         model = Assembly
#         fieldsets = [
#             (None, {'fields': ['name', 'slug', ]})
#         ]
#         prepopulated_fields = {'slug': ('name',), }
#         list_filter = ['name', 'slug']
#         inlines = (DetailInlineAdmin, StandardDetailInlineAdmin, LaborInlineAdmin)
#
#
# class AssemblyAdmin(ImportExportActionModelAdmin):
#     resource_class = AssemblyResource
#     list_display = [field.name for field in Assembly._meta.fields if field.name != "id"]
#     inlines = [DetailInlineAdmin, StandardDetailInlineAdmin, LaborInlineAdmin]
#
#
# admin.site.register(Assembly, AssemblyAdmin)

@admin.register(Labor)
class LaborAdmin(admin.ModelAdmin):
    list_display = ['name', 'machine']


@admin.register(StandardDetail)
class StandardDetailAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount_material', 'unit']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'amount', 'unit', 'get_assemblies', 'get_details', 'get_standard_details',
                    'get_labors')


@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'material', 'amount', 'unit', 'get_labors')


@admin.register(Assembly)
class AssemblyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'amount', 'unit', 'get_details', 'get_standard_details', 'get_labors')

