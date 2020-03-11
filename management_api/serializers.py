from rest_framework import serializers
from management_api.models import VwCurrentDayMenu


class VwCurrentDayMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = VwCurrentDayMenu
        fields = ['rst_name', 'menu']
