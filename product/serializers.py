from rest_framework import serializers
from .models import Category, Product, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "text", "stars", "product"]

    def validate_text(self, value):
        if value is None or not str(value).strip():
            raise serializers.ValidationError("Text is required.")
        return value

    def validate_stars(self, value):
        if value is None:
            raise serializers.ValidationError("Stars is required.")
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Stars must be between 1 and 5.")
        return value


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "description", "price", "category"]

    def validate_title(self, value):
        if value is None or not str(value).strip():
            raise serializers.ValidationError("Title is required.")
        return value

    def validate_price(self, value):
        if value is None:
            raise serializers.ValidationError("Price is required.")
        if value < 0:
            raise serializers.ValidationError("Price must be greater than or equal to 0.")
        return value


class ReviewShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "text", "stars"]


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewShortSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "title", "price", "reviews", "rating"]


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "products_count"]

    def validate_name(self, value):
        if value is None or not str(value).strip():
            raise serializers.ValidationError("Name is required.")
        return value





