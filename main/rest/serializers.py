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


    def update(self, instance, validated_data):
        # Get the list of data IDs from the validated data
        data_ids = validated_data.get('data')

        # If data IDs are provided, add the corresponding Data objects to the instance's data field
        if data_ids:
            instance.data.add(*data_ids)

        return instance
        # return super().update(instance, validated_data)
