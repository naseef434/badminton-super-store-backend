from django.db import models

# Create your models here.


class BasicInfo(models.Model):
    name = models.CharField(max_length=50)
    short_desc = models.CharField(max_length=100, null=True, blank=True)
    thumbnail = models.ImageField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name


class Color(BasicInfo):
    pass


class Size(BasicInfo):
    pass


class Image(models.Model):
    image = models.ImageField()

    def __str__(self) -> str:
        return self.image.path


class Category(BasicInfo):

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.name


class Brand(BasicInfo):

    class Meta:
        verbose_name = 'brand'
        verbose_name_plural = 'brands'

    def __str__(self) -> str:
        return self.name


class Variant(models.Model):
    color = models.ForeignKey(Color, on_delete=models.DO_NOTHING, null=True, blank=True)
    size = models.ForeignKey(Size, on_delete=models.DO_NOTHING, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    images = models.ManyToManyField(Image, blank=True)
    quantity = models.IntegerField(default=0, verbose_name='quantity on hand')

    class Meta:
        verbose_name = 'variant'
        verbose_name_plural = 'variants'

    def __str__(self) -> str:
        if self.color and self.size:
            return f'color: {self.color} | size {self.size}'
        elif self.color:
            return f'color: {self.color}'
        return f'size: {self.size}'


class Product(BasicInfo):
    long_desc = models.TextField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.DO_NOTHING, null=True, blank=True)
    size = models.ForeignKey(Size, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    images = models.ManyToManyField(Image, blank=True)
    variants = models.ManyToManyField(Variant, blank=True)
    price = models.FloatField()
    sale_price = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField(default=0, verbose_name='quantity on hand')

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self) -> str:
        return self.name
