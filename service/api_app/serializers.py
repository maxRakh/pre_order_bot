from rest_framework import serializers

from api_app.models import PreOrder


class PreOrderSerializer(serializers.ModelSerializer):
    day_of_bought = serializers.DateTimeField(read_only=True)
    day_of_canceled = serializers.DateTimeField(read_only=True)

    class Meta:
        model = PreOrder
        fields = '__all__'
        read_only_fields = ('day_of_bought', 'day_of_canceled')
