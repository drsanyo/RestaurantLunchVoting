from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import connection
from management_api.business_logic.repository import ManagementApiRepository


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        repository = ManagementApiRepository(connection.cursor())
        repository.logout(request.user.username)
        content = {'message': 'Ok'}
        return Response(content)



