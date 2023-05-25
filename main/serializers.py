# serializers.py

from rest_framework import serializers
from main.models import Data

class DataSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Data
        fields = '__all__'
