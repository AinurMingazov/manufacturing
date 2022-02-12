from django.db import models
from django.urls import reverse


class Labor(models.Model):
    """Модель описывает операции детали"""
    name = models.CharField(max_length=50)
    machine = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Detail(models.Model):
    """Модель описывает деталь"""
    name = models.CharField(max_length=50)
    material = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=40, null=True, blank=True)

    labors = models.ManyToManyField(
        'Labor',
        through='DetailLabor',
        through_fields=('detail', 'labor',),
    )

    def __str__(self):
        return self.name

    def get_labors(self):
        return "\n".join([p.labors for p in self.labors.all()])

    class Meta:
        ordering = ('name',)


class DetailLabor(models.Model):
    """Модель описывает трудозатраты на изготовления детали"""
    labor = models.ForeignKey("Labor", on_delete=models.SET_NULL,
                              null=True, )
    detail = models.ForeignKey("Detail", on_delete=models.SET_NULL,
                               null=True, )
    time = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ('detail',)


class StandardDetail(models.Model):
    """Модель описывает стандартные детали"""
    name = models.CharField(max_length=200)
    amount_material = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Product(models.Model):
    """Модель описывает изделия"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    amount = models.PositiveIntegerField(default=0, null=True, blank=True)
    unit = models.CharField(max_length=40, null=True, blank=True)
    assemblies = models.ManyToManyField(
        'Assembly',
        through='AssemblyProduct',
        through_fields=('product', 'assembly'),
    )
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
    labors = models.ManyToManyField(
        'Labor',
        through='ProductLabor',
        through_fields=('product', 'labor',),
    )

    def __str__(self):
        return self.name

    def get_labors(self):
        return "\n".join([p.labors for p in self.labors.all()])

    def get_standard_details(self):
        return "\n".join([p.standard_details for p in self.standard_details.all()])

    def get_details(self):
        return "\n".join([p.details for p in self.details.all()])

    def get_assemblies(self):
        return "\n".join([p.assemblies for p in self.assemblies.all()])

    def get_absolute_url(self):
        return reverse('product_detail',
                       kwargs={"product_slug":self.slug})

    class Meta:
        ordering = ('name',)


class ProductDetail(models.Model):
    """Модель описывает детали изделия"""
    product = models.ForeignKey("Product", on_delete=models.SET_NULL, null=True)
    detail = models.ForeignKey("Detail", on_delete=models.SET_NULL, null=True)
    amount_details = models.PositiveIntegerField(default=0)


class ProductStandardDetail(models.Model):
    """Модель описывает стандартные изделия в изделии"""
    product = models.ForeignKey("Product", on_delete=models.SET_NULL, null=True)
    standard_detail = models.ForeignKey("StandardDetail", on_delete=models.SET_NULL, null=True)
    amount_standard_details = models.PositiveIntegerField(default=0)


class ProductLabor(models.Model):
    """Модель описывает трудозатраты на изготовления изделия"""
    labor = models.ForeignKey("Labor", on_delete=models.SET_NULL, null=True, )
    product = models.ForeignKey("Product", on_delete=models.SET_NULL, null=True, )
    time = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ('product',)


class Assembly(models.Model):
    """Модель описывает узел"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    amount = models.PositiveIntegerField(default=0, null=True, blank=True)
    unit = models.CharField(max_length=40, null=True, blank=True)
    details = models.ManyToManyField(
        Detail,
        through='AssemblyDetail',
        through_fields=('assembly', 'detail'),
    )
    standard_details = models.ManyToManyField(
        StandardDetail,
        through='AssemblyStandardDetail',
        through_fields=('assembly', 'standard_detail'),
    )
    labors = models.ManyToManyField(
        'Labor',
        through='AssemblyLabor',
        through_fields=('assembly', 'labor',),
    )

    def __str__(self):
        return self.name

    def get_labors(self):
        return "\n".join([p.labors for p in self.labors.all()])

    def get_standard_details(self):
        return "\n".join([p.standard_details for p in self.standard_details.all()])

    def get_details(self):
        return "\n".join([p.details for p in self.details.all()])

    def get_absolute_url(self):
        return reverse('assembly_detail',
                       kwargs={"assembly_slug": self.slug})

    class Meta:
        ordering = ('name',)


class AssemblyProduct(models.Model):
    """Модель описывает узлы изделия"""
    assembly = models.ForeignKey("Assembly", on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey("Product", on_delete=models.SET_NULL, null=True)
    amount_assemblies = models.PositiveIntegerField(default=0)


class AssemblyDetail(models.Model):
    """Модель описывает детали узла"""
    assembly = models.ForeignKey("Assembly", on_delete=models.SET_NULL, null=True)
    detail = models.ForeignKey("Detail", on_delete=models.SET_NULL, null=True)
    amount_details = models.PositiveIntegerField(default=0)


class AssemblyStandardDetail(models.Model):
    """Модель описывает стандартные изделия в узле"""
    assembly = models.ForeignKey("Assembly", on_delete=models.SET_NULL, null=True)
    standard_detail = models.ForeignKey("StandardDetail", on_delete=models.SET_NULL, null=True)
    amount_standard_details = models.PositiveIntegerField(default=0)


class AssemblyLabor(models.Model):
    """Модель описывает трудозатраты на изготовления узла"""
    labor = models.ForeignKey("Labor", on_delete=models.SET_NULL, null=True, )
    assembly = models.ForeignKey("Assembly", on_delete=models.SET_NULL, null=True, )
    time = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ('assembly',)

