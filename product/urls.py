from django.urls import path
from product import views

urlpatterns = [
    path('product/', views.ProductListAPIView.as_view()),
    path('product/<int:id>/', views.ProductDetailAPIView.as_view()),
    path('categories/', views.CategoryListAPIView.as_view()),
    path('categories/<int:id>/', views.CategoryDetailAPIView.as_view()),
    path('review/', views.ReviewListAPIView.as_view()),
    path('review/<int:id>/', views.ReviewDetailAPIView.as_view()),
]