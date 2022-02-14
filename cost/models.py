from django.db import models
from django.urls import reverse


class Material(models.Model):
    """Модель описывает материал"""
    name = models.CharField(max_length=60)
    unit = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name


class Labor(models.Model):
    """Модель описывает операции детали"""
    name = models.CharField(max_length=60)
    machine = models.CharField(max_length=60, null=True)

    def __str__(self):
        return self.name


class StandardDetail(models.Model):
    """Модель описывает стандартные детали"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Detail(models.Model):
    """Модель описывает деталь"""
    name = models.CharField(max_length=60)
    materials = models.ManyToManyField(
        'Material',
        through='DetailMaterial',
        through_fields=('detail', 'material')
    )
    labors = models.ManyToManyField(
        'Labor',
        through='DetailLabor',
        through_fields=('detail', 'labor')
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class DetailLabor(models.Model):
    """Модель описывает трудозатраты на изготовления детали"""
    detail = models.ForeignKey('Detail', on_delete=models.SET_NULL, null=True)
    labor = models.ForeignKey('Labor', on_delete=models.SET_NULL, null=True)
    time = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)


class DetailMaterial(models.Model):
    """Модель описывает необходимый материал для изготовления детали"""
    detail = models.ForeignKey('Detail', on_delete=models.SET_NULL, null=True)
    material = models.ForeignKey('Material', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)


class Assembly(models.Model):
    """Модель описывает узел"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    materials = models.ManyToManyField(
        'Material',
        through='AssemblyMaterial',
        through_fields=('assembly', 'material')
    )
    details = models.ManyToManyField(
        Detail,
        through='AssemblyDetail',
        through_fields=('assembly', 'detail')
    )
    standard_details = models.ManyToManyField(
        StandardDetail,
        through='AssemblyStandardDetail',
        through_fields=('assembly', 'standard_detail')
    )
    labors = models.ManyToManyField(
        'Labor',
        through='AssemblyLabor',
        through_fields=('assembly', 'labor')
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class AssemblyMaterial(models.Model):
    """Модель описывает материалы узла"""
    assembly = models.ForeignKey('Assembly', on_delete=models.SET_NULL, null=True)
    material = models.ForeignKey('Material', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)


class AssemblyDetail(models.Model):
    """Модель описывает детали узла"""
    assembly = models.ForeignKey('Assembly', on_delete=models.SET_NULL, null=True)
    detail = models.ForeignKey('Detail', on_delete=models.SET_NULL, null=True)
    amount = models.PositiveIntegerField(default=0)


class AssemblyStandardDetail(models.Model):
    """Модель описывает стандартные изделия узла"""
    assembly = models.ForeignKey('Assembly', on_delete=models.SET_NULL, null=True)
    standard_detail = models.ForeignKey('StandardDetail', on_delete=models.SET_NULL, null=True)
    amount = models.PositiveIntegerField(default=0)


class AssemblyLabor(models.Model):
    """Модель описывает трудозатраты на изготовления узла"""
    assembly = models.ForeignKey('Assembly', on_delete=models.SET_NULL, null=True)
    labor = models.ForeignKey('Labor', on_delete=models.SET_NULL, null=True)
    time = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)


class Product(models.Model):
    """Модель описывает изделия"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    materials = models.ManyToManyField(
        'Material',
        through='ProductMaterial',
        through_fields=('product', 'material')
    )
    assemblies = models.ManyToManyField(
        'Assembly',
        through='ProductAssembly',
        through_fields=('product', 'assembly')
    )
    details = models.ManyToManyField(
        Detail,
        through='ProductDetail',
        through_fields=('product', 'detail')
    )
    standard_details = models.ManyToManyField(
        StandardDetail,
        through='ProductStandardDetail',
        through_fields=('product', 'standard_detail')
    )
    labors = models.ManyToManyField(
        'Labor',
        through='ProductLabor',
        through_fields=('product', 'labor')
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail',
                       kwargs={"product_slug": self.slug})

    class Meta:
        ordering = ('name',)


class ProductMaterial(models.Model):
    """Модель описывает материалы узла"""
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    material = models.ForeignKey('Material', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)


class ProductAssembly(models.Model):
    """Модель описывает узлы изделия"""
    assembly = models.ForeignKey('Assembly', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    amount = models.PositiveIntegerField(default=0)


class ProductDetail(models.Model):
    """Модель описывает детали изделия"""
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    detail = models.ForeignKey('Detail', on_delete=models.SET_NULL, null=True)
    amount = models.PositiveIntegerField(default=0)


class ProductStandardDetail(models.Model):
    """Модель описывает стандартные изделия в изделии"""
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    standard_detail = models.ForeignKey('StandardDetail', on_delete=models.SET_NULL, null=True)
    amount = models.PositiveIntegerField(default=0)


class ProductLabor(models.Model):
    """Модель описывает трудозатраты на изготовление изделия"""
    labor = models.ForeignKey('Labor', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    time = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ('product',)


class ProductResources(models.Model):
    """Модель описывает ресурсы необходимые для изготовления изделия"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    materials = models.ManyToManyField(
        'Material',
        through='ProductResourcesMaterial',
        through_fields=('product_resources', 'material')
    )
    standard_details = models.ManyToManyField(
        'StandardDetail',
        through='ProductResourcesStandardDetail',
        through_fields=('product_resources', 'standard_detail')
    )
    labors = models.ManyToManyField(
        'Labor',
        through='ProductResourcesLabor',
        through_fields=('product_resources', 'labor')
    )

    def __str__(self):
        return self.name


class ProductResourcesMaterial(models.Model):
    """Модель описывает необходимый материал для изготовления изделия"""
    product_resources = models.ForeignKey('ProductResources', on_delete=models.SET_NULL, null=True)
    material = models.ForeignKey('Material', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)


class ProductResourcesStandardDetail(models.Model):
    """Модель описывает необходимые стандартные изделия для изготовления изделия"""
    product_resources = models.ForeignKey('ProductResources', on_delete=models.SET_NULL, null=True)
    standard_detail = models.ForeignKey('StandardDetail', on_delete=models.SET_NULL, null=True)
    amount = models.PositiveIntegerField(default=0)


class ProductResourcesLabor(models.Model):
    """Модель описывает необходимые трудозатраты для изготовления изделия"""
    product_resources = models.ForeignKey('ProductResources', on_delete=models.SET_NULL, null=True)
    labor = models.ForeignKey('Labor', on_delete=models.SET_NULL, null=True)
    time = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)


class ManufacturingPlan(models.Model):
    """Модель описывает ресурсы необходимые для выполнения производственного плана"""
    name = models.CharField(max_length=200)
    product_resources = models.ManyToManyField(
        'ProductResources',
        through='ManufacturingPlanProductResources',
        through_fields=('manufacturing_plan', 'product_resources',),
    )

    def __str__(self):
        return self.name


class ManufacturingPlanProductResources(models.Model):
    """Модель описывает количество изделий в плане производства"""
    manufacturing_plan = models.ForeignKey('ManufacturingPlan', on_delete=models.SET_NULL, null=True)
    product_resources = models.ForeignKey('ProductResources', on_delete=models.SET_NULL, null=True)
    amount = models.PositiveIntegerField(default=0)
