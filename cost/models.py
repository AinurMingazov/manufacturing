from django.db import models
from django.urls import reverse
from pytils.translit import slugify


class Material(models.Model):
    """Модель описывает материал"""

    name = models.CharField(max_length=60, unique=True, verbose_name="Наименование")
    slug = models.CharField(max_length=60, unique=True, verbose_name="Поле slug")
    unit = models.CharField(
        max_length=20, default="кг", verbose_name="Единица измерения"
    )
    price_per_meter = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Стоимость за метр",
    )
    price_per_ton = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Стоимость за тонну",
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Material, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("material_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"


class Labor(models.Model):
    """Модель описывает технологические операции"""

    name = models.CharField(max_length=60, unique=True, verbose_name="Наименование")
    slug = models.CharField(max_length=60, unique=True, verbose_name="Поле slug")
    machine = models.CharField(
        max_length=60, unique=True, verbose_name="Наименование оборудования"
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Labor, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.machine}"

    class Meta:
        ordering = ("name",)
        verbose_name = "Трудоемкость"
        verbose_name_plural = "Трудоемкость"


class StandardDetail(models.Model):
    """Модель описывает стандартные детали"""

    name = models.CharField(max_length=100, unique=True, verbose_name="Наименование")
    slug = models.CharField(max_length=100, unique=True, verbose_name="Поле slug")
    unit = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        default="шт.",
        verbose_name="Единица измерения",
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(StandardDetail, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("standard_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "Стандартное изделие"
        verbose_name_plural = "Стандартные изделия"


class Detail(models.Model):
    """Модель описывает деталь"""

    name = models.CharField(max_length=60, unique=True, verbose_name="Наименование")
    slug = models.CharField(max_length=60, unique=True, verbose_name="Поле slug")

    materials = models.ManyToManyField(
        "Material", through="DetailMaterial", through_fields=("detail", "material")
    )
    labors = models.ManyToManyField(
        "Labor", through="DetailLabor", through_fields=("detail", "labor")
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Detail, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("detail_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "Деталь"
        verbose_name_plural = "Детали"


class DetailLabor(models.Model):
    """Модель описывает трудозатраты на изготовления детали"""

    detail = models.ForeignKey(
        "Detail", on_delete=models.SET_NULL, null=True, verbose_name="Деталь"
    )
    labor = models.ForeignKey(
        "Labor", on_delete=models.SET_NULL, null=True, verbose_name="Трудоемкость"
    )
    time = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name="Количество",
    )

    class Meta:
        ordering = ("labor",)
        verbose_name = "Трудоемкость детали"
        verbose_name_plural = "Трудоемкость детали"


class DetailMaterial(models.Model):
    """Модель описывает необходимый материал для изготовления детали"""

    detail = models.ForeignKey(
        "Detail", on_delete=models.SET_NULL, null=True, verbose_name="Деталь"
    )
    material = models.ForeignKey(
        "Material", on_delete=models.SET_NULL, null=True, verbose_name="Материал"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name="Количество",
    )

    class Meta:
        ordering = ("material",)
        verbose_name = "Материал детали"
        verbose_name_plural = "Материалы детали"


class Assembly(models.Model):
    """Модель описывает сборочную единицу"""

    name = models.CharField(max_length=60, unique=True, verbose_name="Наименование")
    slug = models.CharField(max_length=60, unique=True, verbose_name="Поле slug")

    materials = models.ManyToManyField(
        "Material", through="AssemblyMaterial", through_fields=("assembly", "material")
    )
    details = models.ManyToManyField(
        Detail, through="AssemblyDetail", through_fields=("assembly", "detail")
    )
    standard_details = models.ManyToManyField(
        StandardDetail,
        through="AssemblyStandardDetail",
        through_fields=("assembly", "standard_detail"),
    )
    labors = models.ManyToManyField(
        "Labor", through="AssemblyLabor", through_fields=("assembly", "labor")
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Assembly, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("assembly_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "Сборочная единица"
        verbose_name_plural = "Сборочные единицы"


class AssemblyMaterial(models.Model):
    """Модель описывает материалы сборочной единицы"""

    assembly = models.ForeignKey(
        "Assembly",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Сборочная единица",
    )
    material = models.ForeignKey(
        "Material", on_delete=models.SET_NULL, null=True, verbose_name="Материал"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name="Количество",
    )

    class Meta:
        ordering = ("material",)
        verbose_name = "Материал сборочной единицы"
        verbose_name_plural = "Материалы сборочной единицы"


class AssemblyDetail(models.Model):
    """Модель описывает детали сборочной единицы"""

    assembly = models.ForeignKey(
        "Assembly",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Сборочная единица",
    )
    detail = models.ForeignKey(
        "Detail", on_delete=models.SET_NULL, null=True, verbose_name="Деталь"
    )
    amount = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        ordering = ("detail",)
        verbose_name = "Деталь сборочной единицы"
        verbose_name_plural = "Детали сборочной единицы"


class AssemblyStandardDetail(models.Model):
    """Модель описывает стандартные изделия сборочной единицы"""

    assembly = models.ForeignKey(
        "Assembly",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Сборочная единица",
    )
    standard_detail = models.ForeignKey(
        "StandardDetail",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Стандартное изделие",
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name="Количество",
    )

    class Meta:
        ordering = ("standard_detail",)
        verbose_name = "Стандартное изделие сборочной единицы"
        verbose_name_plural = "Стандартные изделия сборочной единицы"


class AssemblyLabor(models.Model):
    """Модель описывает трудозатраты на изготовления сборочной единицы"""

    assembly = models.ForeignKey(
        "Assembly",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Сборочная единица",
    )
    labor = models.ForeignKey(
        "Labor", on_delete=models.SET_NULL, null=True, verbose_name="Трудоемкость"
    )
    time = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name="Количество",
    )

    class Meta:
        ordering = ("labor",)
        verbose_name = "Трудоемкость сборочной единицы"
        verbose_name_plural = "Трудоемкость сборочной единицы"


class Product(models.Model):
    """Модель описывает изделия"""

    name = models.CharField(max_length=100, unique=True, verbose_name="Наименование")
    slug = models.CharField(max_length=100, unique=True, verbose_name="Поле slug")

    materials = models.ManyToManyField(
        "Material", through="ProductMaterial", through_fields=("product", "material")
    )
    assemblies = models.ManyToManyField(
        "Assembly", through="ProductAssembly", through_fields=("product", "assembly")
    )
    details = models.ManyToManyField(
        Detail, through="ProductDetail", through_fields=("product", "detail")
    )
    standard_details = models.ManyToManyField(
        StandardDetail,
        through="ProductStandardDetail",
        through_fields=("product", "standard_detail"),
    )
    labors = models.ManyToManyField(
        "Labor", through="ProductLabor", through_fields=("product", "labor")
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ("name",)
        verbose_name = "Изделие"
        verbose_name_plural = "Изделия"


class ProductMaterial(models.Model):
    """Модель описывает материалы сборочной единицы"""

    product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, null=True, verbose_name="Изделие"
    )
    material = models.ForeignKey(
        "Material", on_delete=models.SET_NULL, null=True, verbose_name="Материал"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name="Количество",
    )

    class Meta:
        ordering = ("material",)
        verbose_name = "Материал изделия"
        verbose_name_plural = "Материалы изделия"


class ProductAssembly(models.Model):
    """Модель описывает сборочной единицы изделия"""

    assembly = models.ForeignKey(
        "Assembly",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Сборочная единица",
    )
    product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, null=True, verbose_name="Изделие"
    )
    amount = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        ordering = ("assembly",)
        verbose_name = "Сборочная единица изделия"
        verbose_name_plural = "Сборочные единицы изделия"


class ProductDetail(models.Model):
    """Модель описывает детали изделия"""

    product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, null=True, verbose_name="Изделие"
    )
    detail = models.ForeignKey(
        "Detail", on_delete=models.SET_NULL, null=True, verbose_name="Деталь"
    )
    amount = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        ordering = ("detail",)
        verbose_name = "Деталь изделия"
        verbose_name_plural = "Детали изделия"


class ProductStandardDetail(models.Model):
    """Модель описывает стандартные изделия в изделии"""

    product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, null=True, verbose_name="Изделие"
    )
    standard_detail = models.ForeignKey(
        "StandardDetail",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Стандартное изделие",
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name="Количество",
    )

    class Meta:
        ordering = ("standard_detail",)
        verbose_name = "Стандартное изделие изделия"
        verbose_name_plural = "Стандартные изделия изделия"


class ProductLabor(models.Model):
    """Модель описывает трудозатраты на изготовление изделия"""

    labor = models.ForeignKey(
        "Labor", on_delete=models.SET_NULL, null=True, verbose_name="Трудоемкость"
    )
    product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, null=True, verbose_name="Изделие"
    )
    time = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name="Количество",
    )

    class Meta:
        ordering = ("labor",)
        verbose_name = "Трудоемкость изделия"
        verbose_name_plural = "Трудоемкость изделия"


class ManufacturingPlan(models.Model):
    """Модель описывает производственный план"""

    name = models.CharField(max_length=200, unique=True, verbose_name="Наименование")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Поле slug")
    products = models.ManyToManyField(
        "Product", through="MPProduct", through_fields=("mp", "product")
    )
    assemblies = models.ManyToManyField(
        "Assembly", through="MPAssembly", through_fields=("mp", "assembly")
    )
    details = models.ManyToManyField(
        Detail, through="MPDetail", through_fields=("mp", "detail")
    )
    labors = models.ManyToManyField(
        "Labor", through="MPLabor", through_fields=("mp", "labor")
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ManufacturingPlan, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plan_detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ("name",)
        verbose_name = "План производства"
        verbose_name_plural = "Планы производства"


class MPProduct(models.Model):
    """Модель описывает изделия производственного плана"""

    mp = models.ForeignKey(
        "ManufacturingPlan",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="План производства",
    )
    product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, null=True, verbose_name="Изделие"
    )
    amount = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        verbose_name = "Изделие плана производства"
        verbose_name_plural = "Изделия плана производства"


class MPAssembly(models.Model):
    """Модель описывает сборочной единицы производственного плана"""

    mp = models.ForeignKey(
        "ManufacturingPlan",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="План производства",
    )
    assembly = models.ForeignKey(
        "Assembly",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Сборочная единица",
    )
    amount = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        verbose_name = "Сборочная единица плана производства"
        verbose_name_plural = "Сборочные единицы плана производства"


class MPDetail(models.Model):
    """Модель описывает детали производственного плана"""

    mp = models.ForeignKey(
        "ManufacturingPlan",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="План производства",
    )
    detail = models.ForeignKey(
        "Detail", on_delete=models.SET_NULL, null=True, verbose_name="Деталь"
    )
    amount = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        verbose_name = "Деталь плана производства"
        verbose_name_plural = "Детали плана производства"


class MPLabor(models.Model):
    """Модель описывает доп. трудозатраты производственного плана"""

    mp = models.ForeignKey(
        "ManufacturingPlan",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="План производства",
    )
    labor = models.ForeignKey(
        "Labor", on_delete=models.SET_NULL, null=True, verbose_name="Трудоемкость"
    )
    time = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name="Количество",
    )

    class Meta:
        ordering = ("mp",)
        verbose_name = "Трудоемкость плана производства"
        verbose_name_plural = "Трудоемкость плана производства"


class MPResources(models.Model):
    """Модель описывает ресурсы необходимые для выполнения производственного плана"""

    name = models.CharField(max_length=100, unique=True, verbose_name="Наименование")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Поле slug")
    materials = models.ManyToManyField(
        "Material",
        through="MPResourcesMaterial",
        through_fields=("mp_resources", "material"),
    )
    standard_details = models.ManyToManyField(
        "StandardDetail",
        through="MPResourcesStandardDetail",
        through_fields=("mp_resources", "standard_detail"),
    )
    labors = models.ManyToManyField(
        "Labor", through="MPResourcesLabor", through_fields=("mp_resources", "labor")
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(MPResources, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "Ресурсы плана производства"
        verbose_name_plural = "Ресурсы планов производства"


class MPResourcesMaterial(models.Model):
    """Модель описывает необходимый материал для выполнения производственного плана"""

    mp_resources = models.ForeignKey(
        "MPResources", on_delete=models.SET_NULL, null=True, verbose_name="Ресурсы"
    )
    material = models.ForeignKey(
        "Material", on_delete=models.SET_NULL, null=True, verbose_name="Материал"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name="Количество",
    )

    class Meta:
        ordering = ("material",)
        verbose_name = "Материал ресурсов плана производства"
        verbose_name_plural = "Материалы ресурсов плана производства"


class MPResourcesStandardDetail(models.Model):
    """Модель описывает необходимые стандартные изделия для выполнения производственного плана"""

    mp_resources = models.ForeignKey(
        "MPResources", on_delete=models.SET_NULL, null=True, verbose_name="Ресурсы"
    )
    standard_detail = models.ForeignKey(
        "StandardDetail",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Стандартное изделие",
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name="Количество",
    )

    class Meta:
        ordering = ("standard_detail",)
        verbose_name = "Материал ресурсов плана производства"
        verbose_name_plural = "Материалы ресурсов плана производства"


class MPResourcesLabor(models.Model):
    """Модель описывает необходимые трудозатраты для выполнения производственного плана"""

    mp_resources = models.ForeignKey(
        "MPResources", on_delete=models.SET_NULL, null=True, verbose_name="Ресурсы"
    )
    labor = models.ForeignKey(
        "Labor", on_delete=models.SET_NULL, null=True, verbose_name="Трудоемкость"
    )
    time = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name="Количество",
    )

    class Meta:
        ordering = ("labor",)
        verbose_name = "Трудоемкость ресурсов плана производства"
        verbose_name_plural = "Трудоемкость ресурсов плана производства"
