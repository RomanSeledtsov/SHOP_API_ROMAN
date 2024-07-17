from django.db import models
from rest_framework.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.PositiveIntegerField(default=150)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField()
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    stars = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'Review for {self.product.title}'

    def clean(self):
        if self.stars < 1 or self.stars > 5:
            raise ValidationError('Stars must be between 1 and 5')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
