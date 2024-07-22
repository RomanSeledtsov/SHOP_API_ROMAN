from django.db import models
from pip._vendor.rich.markup import Tag
from rest_framework.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ProductTag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True, blank=True)
    price = models.PositiveIntegerField(default=150)
    category = models.ForeignKey(Category,
                                 related_name='categories',
                                 on_delete=models.CASCADE),
    tags = models.ManyToManyField(ProductTag,
                                  related_name='products')

    def __str__(self):
        return self.title


STARS = ((i, str(i)) for i in range(1, 6))

class Review(models.Model):
    text = models.CharField(max_length=50)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    stars = models.IntegerField(choices=STARS, null=True, blank=True)

    def __str__(self):
        return self.text



