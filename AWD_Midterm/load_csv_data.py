import os
import django
import csv

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AWD_Midterm.settings')  # Replace 'your_project' with your Django project name
django.setup()

from CreditAnalysis.models import CreditAnalysis

def load_csv_to_database(csv_file_path):
    try:
        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:

                CreditAnalysis.objects.create(
                    cust_id=row['CUST_ID'],
                    balance=row.get('BALANCE', 0),
                    balance_freq=row.get('BALANCE_FREQUENCY', 0),
                    purch=row.get('PURCHASES', 0),
                    onceoff_purch=row.get('ONEOFF_PURCHASES', 0),
                    install_purch=row.get('INSTALLMENTS_PURCHASES', 0),
                    cash_adv=row.get('CASH_ADVANCE', 0),
                    purch_freq=row.get('PURCHASES_FREQUENCY', 0),
                    onceoff_purch_freq=row.get('ONEOFF_PURCHASES_FREQUENCY', 0),
                    purch_install_freq=row.get('PURCHASES_INSTALLMENTS_FREQUENCY', 0),
                    cash_adv_freq=row.get('CASH_ADVANCE_FREQUENCY', 0),
                    cash_adv_tRX=row.get('CASH_ADVANCE_TRX', 0),
                    purch_tRX=row.get('PURCHASES_TRX', 0),
                    cred_limit=row.get('CREDIT_LIMIT', None) or None,
                    payments=row.get('PAYMENTS', 0),
                    min_payments=row.get('MINIMUM_PAYMENTS', None) or None,
                    prc_full_payment=row.get('PRC_FULL_PAYMENT', 0),
                    tenure=row.get('TENURE', 0)
                )
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error loading data for `cust_Id: `{row['CUST_ID']}: {e}")
        print(f"Problematic row data: {row}") 

if __name__ == '__main__':
    csv_file_path = "Financial_Data_Credit_Analysis.csv"
    load_csv_to_database(csv_file_path)
