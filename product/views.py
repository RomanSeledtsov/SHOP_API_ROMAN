from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from product.serializer import CategorySerializer, ProductSerializer, ReviewSerializer, ProductValidateSerializer, \
    ReviewValidateSerializer
from product.models import Category, Product, Review


@api_view(['GET', 'POST'])
def products_list_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = ProductSerializer(products, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        title = serializer.validated_data['title']
        description = serializer.validated_data['description']
        price = serializer.validated_data['price']
        category_id = serializer.validated_data['category']
        tags = serializer.validated_data['tags']

        product = Product.objects.create(title=title, description=description, price=price, category_id=category_id)
        product.tags.set(tags)
        product.save()

        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def products_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'Error message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = ProductSerializer(product, many=False).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(product, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(status=status.HTTP_200_OK, data={'errors': serializer.errors})
        # return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        product.detail.title = serializer.validated_data['title']
        product.detail.description = serializer.validated_data['description']
        product.detail.price = serializer.validated_data['price']
        product.detail.category_id = serializer.validated_data['category_id']
        product.detail.tags.set(serializer.validated_data['tags'])
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, data={'product_id': product.id})


@api_view(['GET', 'POST'])
def reviews_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewSerializer(reviews, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})
        print(request.data)

        text = serializer.validated_data['text']
        product_id = serializer.validated_data['product']
        stars = serializer.validated_data['stars']
        Review.objects.create(product_id=product_id, stars=stars, text=text)
        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def reviews_detail_api_view(request, id, self):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'Error message': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = ReviewSerializer(review, many=False).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        review_detail = self.get_object()
        serializer = ReviewValidateSerializer(review, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})

        review_detail.text = serializer.validated_data['text']
        review_detail.product_id = serializer.validated_data['product']
        review_detail.stars = serializer.validated_data['stars']
        review_detail.save()
        return Response(status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, data={'review_id': review.id})


@api_view(['GET', 'POST'])
def categories_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        data = CategorySerializer(categories, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'POST':

        name = request.data.get('name')
        category = Category.objects.create(name=name)
        category.save()
        return Response(status=status.HTTP_201_CREATED, data={'category_id': category.id})


@api_view(['GET', 'PUT', 'DELETE'])
def categories_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'Error message': 'Category not found'},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = CategorySerializer(category, many=False).data
        return Response(data=data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, data={'category_id': category.id})
