import matplotlib.pyplot as plt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CreditAnalysis
from .serializer import CreditAnalysisSerializer
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Avg, Sum
from decimal import Decimal
from rest_framework.pagination import PageNumberPagination

# VIEWS TO MAKE FOR CREDIT ANALYSIS APPLICATION
class CustomPagination(PageNumberPagination):
    page_size = 20 #Show 20 entries

# Main Page
def main_page(request):
    # Define all endpoints to appear on the main page
    endpoints = [
        {"name": "GET - Retrieve all customers making low payments, high balances and with loan terms longer than approx 8 years", "url": reverse('get_all_data_filter'),
            "description": [
                "This identifies customers who are potentially struggling to manage their debt."
            ]},
        {"name": "POST - Create New Data: A POST method used to add a new entry to the database.", "url": reverse('create_data')},
        {"name": "DELETE/UPDATE - Delete/Update Data: Updates & Deletes a specific entry by entering a primary key to the url.", "url": reverse('data_detail', kwargs={'pk': 5})}, #Primary key = 5
        {"name": "GET - Filter Data: A GET method that allows filtering data based on financial metrics. It is used by adding query parameters to the url.", "url": reverse('filter_data') + "?balance<1000&purch>5000"},  # query paramaters Added
        {"name": "GET - Credit Analysis Graphs: A GET method to provide visual analytics by using matplotlib to generate and display graphs", "url": reverse('credit_analysis_graphs'),
            "description": [
                "Visualize how much of the credit limit is being used.",
                "Visualize credit utilization and spending patterns.",
                "RISK INDICATORS: Visualize the frequency of high risk transactions.",
                "Analyze the frequency of different transactions and understand how often customers engage with credit."]}
    ]
    return render(request, 'main_page.html', {"endpoints": endpoints})

# ENDPOINTS

#RETRIEVE DATA (GET)
@api_view(['GET'])
def get_all_data_filter(request):
    # Optimize to load data in smaller chunks
    paginator = CustomPagination()

    # Get query parameters
    queryset = CreditAnalysis.objects.all()

    # Aggregation
    avg_balance = CreditAnalysis.objects.aggregate(avg_balance=Sum('balance'))['avg_balance']
    avg_payments = CreditAnalysis.objects.aggregate(avg_payments=Sum('payments') + Sum('min_payments') + Sum('prc_full_payment'))['avg_payments']
    avg_tenure = CreditAnalysis.objects.aggregate(avg_tenure=Sum('tenure'))['avg_tenure']

    if avg_balance:
        high_balance_threshold = Decimal(avg_balance) * Decimal(0.75)  # 75% above average
    else:
        high_balance_threshold = None

    if avg_payments:
        low_payment_threshold = Decimal(avg_payments) * Decimal(0.25)  # 25% below average
    else:
        low_payment_threshold = None

    if avg_tenure:
        high_tenure_threshold = Decimal(avg_tenure) * Decimal(1.25)  # 25% above average
    else:
        high_tenure_threshold = None

    queryset = CreditAnalysis.objects.all()

    balance = request.query_params.get('balance')
    payments = request.query_params.get('payments')
    min_payments = request.query_params.get('min_payments')
    prc_full_payments = request.query_params.get('prc_full_payments')
    tenure = request.query_params.get('tenure')

    # Filtering based on thresholds
    if payments:
        queryset = queryset.filter(payments__lt=low_payment_threshold)
    if min_payments:
        queryset = queryset.filter(min_payments__lt=low_payment_threshold)
    if prc_full_payments:
        queryset = queryset.filter(prc_full_payment__lt=low_payment_threshold)
    if balance:
        queryset = queryset.filter(balance__gt=high_balance_threshold)
    if tenure:
        queryset = queryset.filter(tenure__gt=high_tenure_threshold)

    serializer = CreditAnalysisSerializer(queryset, many=True)
    return Response(serializer.data)

# FILTER DATA (GET)
# - Supply figures in url e.g. ?balance=1000&purch=5000&credit_Limit=10000&min_Payments=500
@api_view(['GET'])
def filter_data(request):
    paginator = CustomPagination()
    
    # Query Parameters from models
    balance = request.GET.get('balance')
    purch = request.GET.get('Purchases')
    cred_limit = request.GET.get('Credit Limit')
    min_payments = request.GET.get('Minimum Payments')

    #Build Filters
    filters = {}
    if balance:
        filters['balance__gte'] = balance
    if purch:
        filters['purchases__gte'] = purch
    if cred_limit:
        filters['credit_limit__gte'] = cred_limit
    if min_payments:
        filters['min_payments__gte'] = min_payments

    # Apply filter and get data
    filtered_data = CreditAnalysis.objects.filter(**filters)
    serializer = CreditAnalysisSerializer(filtered_data, many=True)
    return Response(serializer.data)

#ADD NEW DATA (POST)
@api_view(['POST'])
def create_data(request):
    serializer = CreditAnalysisSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def data_detail(request, pk):
    try:
        CreditAnalysis_data = CreditAnalysis.objects.get(pk = pk)
    except CreditAnalysis.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Finding a specific user
    if request.method == 'GET':
        serializer = CreditAnalysisSerializer(CreditAnalysis_data)
        return Response(serializer.data)
    
    # UPDATE DATA (PUT) - Have to enter pk
    elif request.method == 'PUT':
        serializer = CreditAnalysisSerializer(CreditAnalysis_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #DELETE DATA (DELETE)
    elif request.method == 'DELETE':
        CreditAnalysis_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Calculate Credit analaysis and show a graph
@api_view(['GET'])
def credit_analysis(request):
    paginator = CustomPagination()
    credit_analysis_data = CreditAnalysis.objects.all()
                                     
    balance = [item.balance for item in credit_analysis_data]
    balance_freq = [item.balance_freq for item in credit_analysis_data]
    purch = [item.purch for item in credit_analysis_data]
    onceoff_purch = [item.onceoff_purch for item in credit_analysis_data]
    install_purch = [item.install_purch for item in credit_analysis_data]
    cash_adv = [item.cash_adv for item in credit_analysis_data]
    purch_freq = [item.purch_freq for item in credit_analysis_data]
    onceoff_purch_freq = [item.onceoff_purch_freq for item in credit_analysis_data]
    purch_install_freq = [item.purch_install_freq for item in credit_analysis_data]
    cash_adv_freq = [item.cash_adv_freq for item in credit_analysis_data]
    cash_adv_tRX = [item.cash_adv_tRX for item in credit_analysis_data]
    purch_tRX = [item.purch_tRX for item in credit_analysis_data]
    cred_limit = [item.cred_limit for item in credit_analysis_data]
    payments = [item.payments for item in credit_analysis_data]
    min_payments = [item.min_payments for item in credit_analysis_data]
    prc_full_payment = [item.prc_full_payment for item in credit_analysis_data]
    tenure = [item.tenure for item in credit_analysis_data]
    
    # GRAPHS

    # TODAY
    #Transaction Frequency: Analyze the frequency of different transactions
    # (purchases, once-off purchases, installments, cash advances)
    # understand how often customers engage with credit.
    avg_purch_freq = sum(purch) / len(credit_analysis_data) if len(credit_analysis_data) > 0 else 0
    avg_onceoff_purch_freq = sum(onceoff_purch) / len(credit_analysis_data) if len(credit_analysis_data) > 0 else 0
    avg_install_purch_freq = sum(install_purch) / len(credit_analysis_data) if len(credit_analysis_data) > 0 else 0
    avg_cash_adv_freq = sum(cash_adv) / len(credit_analysis_data) if len(credit_analysis_data) > 0 else 0

    plt.figure(figsize=(10, 6))
    plt.bar(['Purchases', 'Once-off Purchases', 'Installments', 'Cash Advances'], 
    [avg_purch_freq, avg_onceoff_purch_freq, avg_install_purch_freq, avg_cash_adv_freq])
    plt.ylabel('Frequency')
    plt.title('Average Transaction Frequency')
    plt.savefig('CreditAnalysis/static/graph4.png')
    plt.close()

    # CREDIT UTILIZATION: Plotting Balance VS Credit Limit
    plt.figure(figsize=(10, 6))
    plt.scatter(balance, cred_limit, edgecolors='k', alpha=0.5)
    plt.title('Balance vs Credit Limit', fontsize=14)
    plt.xlabel('Balance', fontsize=12, color='black')
    plt.ylabel('Credit Limit', fontsize=12, color='black')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.savefig('CreditAnalysis/static/graph1.png')
    plt.close()

    # TRANSACTION ANALYSIS: Plotting Purchases VS Cash Advances
    plt.figure(figsize=(10, 6))
    plt.scatter(purch, cash_adv, edgecolors='k', alpha=0.5)
    
    # Adding labels and title
    plt.xlabel('Purchases')
    plt.ylabel('Cash Advances')
    plt.title('Purchases vs. Cash Advances')
    plt.savefig('CreditAnalysis/static/graph2.png')
    plt.close()
 
    # TRANSACTION FREQUENCIES: Plotting Purchase Frequency VS Cash Advance Frequency (Risk Indicators)
    # Visualize the frequency of high risk transactions
    plt.figure(figsize=(10, 6))
    x_positions = range(len(purch_freq))  # Create positions for the x-axis

    # Bar for Purchase Frequency
    plt.bar(x_positions, purch_freq, label='Purchase Frequency', color='blue', alpha=0.8, width=0.4, align='center')
    plt.bar([x + 0.4 for x in x_positions], cash_adv_freq, label='Cash Advance Frequency', color='red', alpha=0.5, width=0.4)
    plt.xlabel('Purchase Frequency', color='black')  
    plt.ylabel('Cash Advance Frequency', color='black')
    plt.title('Purchase Frequency VS Cash Advance Frequency')
    plt.legend()  
    plt.savefig('CreditAnalysis/static/graph3.png')
    plt.close()

    # Render the template with the graphs
    return render(request, 'credit_analysis_graphs.html',{
        'graph1': '/static/graph1.png',
        'graph2': '/static/graph2.png',
        'graph3': '/static/graph3.png',
        'graph4': '/static/graph4.png'
    })