# api/serializers.py
from rest_framework import serializers

class TransactionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    date = serializers.DateField()
    description = serializers.CharField()
    category = serializers.CharField()
    type = serializers.CharField()
    source = serializers.CharField()
