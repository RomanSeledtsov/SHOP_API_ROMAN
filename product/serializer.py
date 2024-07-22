from django.core.exceptions import ValidationError
from rest_framework import serializers
from product.models import Category, Product, Review, ProductTag
from django.db.models import Avg


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['name', 'count_products']

    def get_products_count(self, count):
        return count.products.count()


class CategoryValueSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=1, max_length=50)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product', 'text', 'stars']


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=1, max_length=100)
    product = serializers.IntegerField(min_value=1)
    stars = serializers.IntegerField(min_value=1, max_value=5)


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category', 'id', 'reviews', 'average_rating']

    def get_average_rating(self, product):
        reviews = product.reviews.all()
        if reviews:
            sum_reviews = sum(i.stars for i in reviews)
            average_rating = sum_reviews / len(reviews)
            return average_rating
        return None


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=1, max_length=50)
    description = serializers.CharField(min_length=1, max_length=100, required=False)
    price = serializers.IntegerField(min_value=1)
    category = serializers.IntegerField(min_value=1)
    tags = serializers.ListField(child=serializers.IntegerField(min_value=1), required=False)

    def validate_tags(self, tags):
        tag_a = set(tags)
        tag_db = ProductTag.objects.filter(id__in=tag_a)
        if len(tag_db) != len(tags):
            raise ValidationError("Tags does not exist ")
        return tags
