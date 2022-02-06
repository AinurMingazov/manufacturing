from django.db import models
from django.urls import reverse


class LaborCosts(models.Model):
    """Модель описывает трудозатраты"""
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60, unique=True)
    machine = models.CharField(max_length=50, null=True)
    mach_slug = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class DetailLaborCosts(models.Model):
    """Модель описывает трудозатраты изготовления детали"""
    labor = models.ForeignKey("LaborCosts", on_delete=models.SET_NULL,
                              null=True, )
    detail = models.ForeignKey("Detail", on_delete=models.SET_NULL,
                               null=True, )
    time_details = models.PositiveIntegerField(default=0)
    cost_details = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('time_details',)


class Detail(models.Model):
    """Модель описывает деталь"""
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60, unique=True)
    material = models.CharField(max_length=200)
    mat_slug = models.CharField(max_length=200, null=True, blank=True)
    amount_material = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=40, null=True, blank=True)
    weight = models.PositiveIntegerField(default=0, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    detail_labor_costs = models.ManyToManyField(
        'LaborCosts',
        through='DetailLaborCosts',
        through_fields=('detail','labor',),
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cost:product_detail',
                       args=[self.slug])

    class Meta:
        ordering = ('name',)


class StandardDetail(models.Model):
    """Модель описывает стандартные детали"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    amount_material = models.PositiveIntegerField(default=0, null=True, blank=True)
    unit = models.CharField(max_length=40, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('store:tool_detail',
    #                    args=[self.id, self.slug])

    class Meta:
        ordering = ('name',)


# class ProductionPlan(models.Model):
#     """Модель описывает план производства"""
#     name = models.CharField(max_length=200)
#     slug = models.SlugField(max_length=200, unique=True)
#     details = models.ManyToManyField(
#         'Product',
#         through='ProductPlan',
#         through_fields=('productionplan', 'product'),
#     )
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)


class Product(models.Model):
    """Модель описывает изделия"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    amount = models.PositiveIntegerField(default=0, null=True, blank=True)
    unit = models.CharField(max_length=40, null=True, blank=True)
    details = models.ManyToManyField(
        Detail,
        through='ProductDetail',
        through_fields=('product', 'detail'),
    )

    standard_details = models.ManyToManyField(
        StandardDetail,
        through='ProductStandardDetail',
        through_fields=('product', 'standard_detail'),
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail',
                       kwargs={"product_slug":self.slug})

    class Meta:
        ordering = ('name',)


class ProductDetail(models.Model):
    """Модель описывает детали изделия"""
    product = models.ForeignKey("Product", on_delete=models.SET_NULL,
                                null=True,)
    detail = models.ForeignKey("Detail", on_delete=models.SET_NULL,
                               null=True,)
    amount_details = models.PositiveIntegerField(default=0)

# class ProductionPlan(models.Model):
#     """Модель описывает изделия в плане производства"""
#     product = models.ForeignKey("Product", on_delete=models.SET_NULL,
#                                 null=True,)
#     productionplan = models.ForeignKey("ProductionPlan", on_delete=models.SET_NULL,
#                                null=True,)
#     amount_products = models.PositiveIntegerField(default=0)



class ProductStandardDetail(models.Model):
    """Модель описывает стандартные изделия в изделии"""
    product = models.ForeignKey("Product", on_delete=models.SET_NULL,
                                 null=True)
    standard_detail = models.ForeignKey("StandardDetail", on_delete=models.SET_NULL,
                                        null=True)
    amount_standard_detail = models.PositiveIntegerField(default=1)
