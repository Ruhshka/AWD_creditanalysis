from django.db import models

# Create your models here.
# models to match the dataset
class CreditAnalysis(models.Model):
    cust_id = models.CharField(max_length=6, null=False, unique=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    balance_freq = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    purch = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    onceoff_purch = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    install_purch = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    cash_adv = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    purch_freq = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    onceoff_purch_freq = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    purch_install_freq = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    cash_adv_freq = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    cash_adv_tRX = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    purch_tRX = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    cred_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    payments = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    min_payments = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    prc_full_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    tenure = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.cust_id