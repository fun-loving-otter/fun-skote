from rest_framework import serializers

from main.models import Data, DataList



class DataSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Data
        fields = '__all__'
        datatables_always_serialize = ('id',)



class DataListSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')

    class Meta:
        model = DataList
        fields = ['data', 'creator']
