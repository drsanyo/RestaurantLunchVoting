from django.urls import path
from management_api import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('create_restaurant/', views.CreateRestaurant.as_view(), name='CreateRestaurant'),
    path('upload_menu/', views.UploadMenu.as_view(), name='UploadMenu'),
    path('add_employee/', views.AddEmployee.as_view(), name='AddEmployee'),
    path('current_day_menu/', views.CurrentDayMenu.as_view(), name='CurrentDayMenu'),
    path('vote/', views.Vote.as_view(), name='Vote'),
    path('current_day_winner/', views.CurrentDayWinner().as_view(), name='CurrentDayWinner'),
]