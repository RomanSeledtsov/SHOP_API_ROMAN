from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products_list_api_view),
    path('products/<int:id>/', views.products_detail_api_view),
    path('category/', views.categories_list_api_view),
    path('category/<int:id>/', views.categories_detail_api_view),
    path('review/', views.reviews_list_api_view),
    path('review/<int:id>/', views.reviews_detail_api_view),
]