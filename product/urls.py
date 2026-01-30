from django.urls import path
from . import views

urlpatterns = [
    # categories
    path('categories/', views.category_list),
    path('categories/<int:id>/', views.category_detail),

    # products
    path('products/', views.product_list),
    path('products/<int:id>/', views.product_detail),

    # reviews
    path('reviews/', views.review_list),
    path('reviews/<int:id>/', views.review_detail),

    # DZ2 endpoint
    path('products/reviews/', views.products_with_reviews),
]




