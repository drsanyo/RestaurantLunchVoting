from django.urls import path
from management_api import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('create_restaurant/', views.CreateRestaurant.as_view(), name='CreateRestaurant'),
]