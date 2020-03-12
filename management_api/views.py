from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import connection
from management_api.business_logic.repository import ManagementApiRepository
from rest_framework import status
from django.contrib.auth.models import User
from management_api.models import VwCurrentDayMenu
from management_api.serializers import VwCurrentDayMenuSerializer
from django.conf import settings


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


class AddEmployee(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        employee_name = request.data.get('name')
        if not employee_name:
            return Response('Employee name cannot be empty, please set query parameter "name"',
                            status.HTTP_400_BAD_REQUEST)

        employee_password = request.data.get('password')
        if not employee_password:
            return Response('Employee password cannot be empty, please set query parameter "password"',
                            status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(
                username=employee_name,
                password=employee_password)
            content = {'new user_id': user.id}
            return Response(content)
        except Exception as e:
            return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


class CurrentDayMenu(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            current_day_menu = VwCurrentDayMenu.objects.all()
            serializer = VwCurrentDayMenuSerializer(current_day_menu, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


class Vote(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        restaurant_name = request.query_params.get('restaurant')
        if not restaurant_name:
            return Response('Restaurant name cannot be empty, please set query parameter "restaurant"',
                            status.HTTP_400_BAD_REQUEST)

        try:
            repository = ManagementApiRepository(connection.cursor())
            votes_count = repository.user_vote(restaurant_name, request.user.username)
            content = {'Restaurant votes count': votes_count}
            return Response(content)
        except Exception as e:
            return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


class CurrentDayWinner(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            repository = ManagementApiRepository(connection.cursor())
            winner = repository.current_day_winner(settings.SKIP_LAST_CONSECUTIVE_WORKING_DAYS)
            content = {'Winner': winner}
            return Response(content)
        except Exception as e:
            return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
