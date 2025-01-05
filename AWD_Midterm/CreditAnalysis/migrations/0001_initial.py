# Generated by Django 5.1.4 on 2025-01-02 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CreditAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cust_id', models.CharField(max_length=6)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('balance_freq', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('purch', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('onceoff_purch', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('install_purch', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('cash_adv', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('purch_freq', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('onceoff_purch_freq', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('purch_install_freq', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('cash_adv_freq', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('cash_adv_tRX', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('purch_tRX', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('cred_limit', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('payments', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('min_payments', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('prc_full_payment', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('tenure', models.IntegerField(default=0, null=True)),
            ],
        ),
    ]
