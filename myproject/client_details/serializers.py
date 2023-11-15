from rest_framework import serializers
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'org_name', 'project_name', 'description', 'estimation']
