from django.db.models import Avg, Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Category, Product, Review
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
    ProductWithReviewsSerializer
)


# ---------- Categories ----------
@api_view(['GET'])
def category_list(request):
    # products_count по ТЗ
    categories = Category.objects.annotate(products_count=Count('products'))
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def category_detail(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({'detail': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    # в detail products_count не требовали, но пусть будет красиво:
    category.products_count = category.products.count()
    serializer = CategorySerializer(category)
    return Response(serializer.data)


# ---------- Products ----------
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({'detail': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product)
    return Response(serializer.data)


# /api/v1/products/reviews/  (ДЗ2)
@api_view(['GET'])
def products_with_reviews(request):
    products = Product.objects.annotate(
        rating=Avg('reviews__stars')
    ).prefetch_related('reviews')

    # если нет отзывов, rating будет None — можно оставить так, это нормально
    serializer = ProductWithReviewsSerializer(products, many=True)
    return Response(serializer.data)


# ---------- Reviews ----------
@api_view(['GET'])
def review_list(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def review_detail(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response({'detail': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ReviewSerializer(review)
    return Response(serializer.data)




