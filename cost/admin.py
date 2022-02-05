from django.contrib import admin

from cost.models import Detail, Product, StandardDetail, LaborCosts


class DetailInlineAdmin(admin.TabularInline):
    model = Product.details.through


class LaborCostsInlineAdmin(admin.TabularInline):
    model = Detail.detail_labor_costs.through


class StandardDetailInlineAdmin(admin.TabularInline):
    model = Product.standard_details.through


@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'slug', 'material', 'amount_material', 'unit', 'weight', 'price']})
    ]
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['name', 'slug']
    inlines = (LaborCostsInlineAdmin,)


@admin.register(LaborCosts)
class LaborCostsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['name', 'slug']


@admin.register(StandardDetail)
class StandardDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'amount_material', 'unit', 'price']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['name', 'slug']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'slug', 'amount', 'unit', 'price']})
    ]
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['name', 'slug']
    inlines = (DetailInlineAdmin, StandardDetailInlineAdmin)


