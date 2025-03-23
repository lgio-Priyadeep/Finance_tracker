from django.shortcuts import render

# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TransactionSerializer
from app.services import add_manual_transaction, estimate_tax, fetch_bank_transactions
# Import other necessary functions from your services module

class TransactionCreateView(APIView):
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                txn_id = add_manual_transaction(
                    data['user_id'],
                    data['amount'],
                    data['description'],
                    data['category'],
                    txn_date=data.get('date'),
                    txn_type=data.get('type', 'expense'),
                    source=data.get('source', 'cash')
                )
                return Response({"transaction_id": txn_id}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaxEstimateView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        tax_rate = request.query_params.get('tax_rate', 0.1)
        try:
            tax_info = estimate_tax(int(user_id), float(tax_rate))
            return Response(tax_info, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BankTransactionsView(APIView):
    def get(self, request):
        try:
            transactions = fetch_bank_transactions()
            return Response(transactions, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
