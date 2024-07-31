from django.urls import path
from users import views

urlpatterns = [
    path('register/', views.RegistrationAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('confirm_sms/', views.ConfirmSMSAPIView.as_view()),
]