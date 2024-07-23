from django.urls import path
from users import views

urlpatterns = [
    path('register/', views.registration_api_view),
    path('login/', views.login_api_view),
    path('confirm_sms/', views.confirm_sms_api_view),
]