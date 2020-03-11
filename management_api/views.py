from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import connection
from management_api.business_logic.repository import ManagementApiRepository
from rest_framework import status
from django.contrib.auth.models import User


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            repository = ManagementApiRepository(connection.cursor())
            repository.logout(request.user.username)
            content = {'message': 'Ok'}
            return Response(content)
        except Exception as e:
            return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateRestaurant(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        restaurant_name = request.query_params.get('name')
        if not restaurant_name:
            return Response('Restaurant name cannot be empty, please set query parameter "name"',
                            status.HTTP_400_BAD_REQUEST)

        try:
            repository = ManagementApiRepository(connection.cursor())
            new_restaurant_id = repository.create_restaurant(restaurant_name)
            content = {'new_restaurant_id': new_restaurant_id}
            return Response(content)
        except Exception as e:
            return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


class UploadMenu(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        restaurant_name = request.query_params.get('restaurant')
        if not restaurant_name:
            return Response('Restaurant name cannot be empty, please set query parameter "restaurant"',
                            status.HTTP_400_BAD_REQUEST)

        try:
            repository = ManagementApiRepository(connection.cursor())
            for file_name in request.FILES:
                repository.upload_menu(
                    restaurant_name,
                    request.user.username,
                    file_name,
                    request.FILES[file_name].read())
            content = {'message': 'Ok'}
            return Response(content)
        except Exception as e:
            return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)