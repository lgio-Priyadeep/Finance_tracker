# api/urls.py
from django.urls import path
from .views import TransactionCreateView, TaxEstimateView, BankTransactionsView

urlpatterns = [
    path('transactions/', TransactionCreateView.as_view(), name='create_transaction'),
    path('tax/', TaxEstimateView.as_view(), name='estimate_tax'),
    path('bank-transactions/', BankTransactionsView.as_view(), name='fetch_bank_transactions'),
]
