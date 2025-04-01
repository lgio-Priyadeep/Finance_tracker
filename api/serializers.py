# api/serializers.py
from rest_framework import serializers

class TransactionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    txn_date = serializers.DateField()
    description = serializers.CharField()
    category = serializers.CharField()
    txn_type = serializers.CharField()
    source = serializers.CharField()
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive.")
        return value
