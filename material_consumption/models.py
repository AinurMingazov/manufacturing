from django.db import models
from django.urls import reverse


class Detail(models.Model):
    """Модель описывает деталь"""
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60, unique=True)
    material = models.CharField(max_length=200)
    amount_material = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=40)
    weight = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
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


# class StandardDetail(models.Model):
#     """Модель описывает стандартные детали"""
#     name = models.CharField(max_length=200)
#     slug = models.SlugField(max_length=200, unique=True)
#     amount_material = models.PositiveIntegerField(default=0)
#     unit = models.CharField(max_length=40)
#     price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
#     available = models.BooleanField(default=True)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.name
#
#     # def get_absolute_url(self):
#     #     return reverse('store:tool_detail',
#     #                    args=[self.id, self.slug])
#
#     class Meta:
#         ordering = ('name',)


class Product(models.Model):
    """Модель описывает стандартные изделия"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    amount = models.PositiveIntegerField(default=0)
    unit = models.CharField(max_length=40)
    details = models.ManyToManyField(
        Detail,
        through='ProductDetail',
        through_fields=('product', 'detail' ),
    )

    # standard_details = models.ManyToManyField(
    #     StandardDetail,
    #     through='ProductStandardDetail',
    #     through_fields=('amount',),
    # )
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
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


class ProductDetail(models.Model):
    """Модель описывает детали изделия"""
    product = models.ForeignKey("Product", on_delete=models.SET_NULL,
                                null=True,)
    detail = models.ForeignKey("Detail", on_delete=models.SET_NULL,
                               null=True,)
    amount_details = models.PositiveIntegerField(default=0)


# class ProductStandardDetail(models.Model):
#     """Модель описывает стандартные изделия в изделии"""
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL,
#                                 related_name='product_standart_detail', null=True)
#     standart_detail = models.ForeignKey(StandardDetail, on_delete=models.SET_NULL,
#                                related_name='standart_detail_product', null=True)
#     amount = models.PositiveIntegerField(default=1)
