from rest_framework import serializers
from product.models import Category, Product, Review
from django.db.models import Avg


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_products_count(self, count):
        return count.products.count()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category', 'id', 'reviews', 'average_rating']
        depth = 1

    def get_average_rating(self, product):
        reviews = Review.objects.filter(product=product)
        if reviews.exists():
            average_rating = reviews.aggregate(Avg('stars'))['stars__avg']
            return average_rating or 0
        return 0
