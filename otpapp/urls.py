from django.conf.urls import  url
from .views import LoginUser, VerifyUser, RegisterUser, VerifyToken
from django.urls import path

urlpatterns = [
    # Auth Routes
    # path('', views.index, name ='index'),
    path('api/v.1/auth/register', RegisterUser.as_view(), name = 'register'),
    path('api/v.1/auth/verify/token', VerifyToken.as_view(), name = 'verify_token'),
    path('api/v.1/auth/verify', VerifyUser.as_view(), name = 'verify'),
    path('api/v.1/auth/login', LoginUser.as_view(), name = 'login'),
]
