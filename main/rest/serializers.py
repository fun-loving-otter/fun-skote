from rest_framework import serializers

from main.models import Data, DataList, DataColumnVisibility



class DataSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    def __init__(self, *args, hide_fields=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.hide_fields = hide_fields


    class Meta:
        model = Data
        fields = '__all__'
        datatables_always_serialize = ('id',)


    def to_representation(self, instance):
        '''
        Fields that should have "Add to list to reveal" button on them instead of actual data
        '''
        data = super().to_representation(instance)
        if self.hide_fields:
            for field in Data._hidden_fields:
                if data.get(field):
                    data[field] = "*hidden*"
        return data




class DataListSerializer(serializers.ModelSerializer):
    '''
    Used to add Data object to DataList
    '''
    class Meta:
        model = DataList
        fields = ['data']


    def update(self, instance, validated_data):
        # Get the list of data IDs from the validated data
        data_ids = validated_data.get('data')

        # If data IDs are provided, add the corresponding Data objects to the instance's data field
        if data_ids:
            instance.data.add(*data_ids)

        return instance



class DataFiltersSerializer(serializers.Serializer):
    filters = serializers.JSONField()

    def validate_filters(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Filters must be an object")

        return value



class DataColumnVisibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DataColumnVisibility
        fields = ['visible']
