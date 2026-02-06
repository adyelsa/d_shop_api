

from django.db.models import Avg, Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Category, Product, Review
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
    ProductWithReviewsSerializer,
)


@api_view(["GET", "POST"])
def category_list(request):
    if request.method == "GET":
        categories = Category.objects.annotate(products_count=Count("products"))
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    serializer = CategorySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def category_detail(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        data = CategorySerializer(category).data
        data["products_count"] = category.products.count()
        return Response(data)

    if request.method == "PUT":
        serializer = CategorySerializer(category, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        data = serializer.data
        data["products_count"] = category.products.count()
        return Response(data)

    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def product_list(request):
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    serializer = ProductSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def product_detail(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def products_with_reviews(request):
    products = (
        Product.objects.annotate(rating=Avg("reviews__stars"))
        .prefetch_related("reviews")
    )
    serializer = ProductWithReviewsSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
def review_list(request):
    if request.method == "GET":
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    serializer = ReviewSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def review_detail(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response({"detail": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = ReviewSerializer(review, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

    review.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)




