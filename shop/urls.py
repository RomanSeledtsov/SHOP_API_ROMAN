from django.contrib import admin
from django.urls import path, include
from product import views

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/v1/categories/', include('product.urls')),
#     path('api/v1/categories/<int:id>/', views.categories_detail_api_view),
#     path('api/v1/products/',include('product.urls')),
#     path('api/v1/products/<int:id>/', views.products_detail_api_view),
#     path('api/v1/reviews/', include('product.urls')),
#     path('api/v1/reviews/<int:id>/', views.reviews_detail_api_view),
#     path('api/v1/users/', include('users.urls')),
# ]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('product.urls')),
    path('api/v1/users/', include('users.urls')),
]