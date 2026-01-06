"""
Initial migration for POS System Django models
Creates all database tables
"""
from django.db import migrations, models
import django.db.models.deletion
from django.core.validators import MinValueValidator
from decimal import Decimal


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('position', models.CharField(choices=[('Admin', 'Admin'), ('Cashier', 'Cashier')], max_length=20)),
                ('password_hash', models.CharField(max_length=128)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'employees',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(db_index=True, max_length=20, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'customers',
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('discount_percentage', models.DecimalField(decimal_places=2, default=10.0, max_digits=5)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'coupons',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField(db_index=True, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0.01'))])),
                ('stock_sale', models.IntegerField(default=0, validators=[MinValueValidator(0)])),
                ('stock_rental', models.IntegerField(default=0, validators=[MinValueValidator(0)])),
                ('item_type', models.CharField(choices=[('Sale', 'Sale'), ('Rental', 'Rental'), ('Both', 'Both')], default='Both', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'items',
            },
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, validators=[MinValueValidator(1)])),
                ('rental_date', models.DateField()),
                ('due_date', models.DateField()),
                ('return_date', models.DateField(blank=True, null=True)),
                ('is_returned', models.BooleanField(default=False)),
                ('late_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rentals', to='pos_system.customer')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rentals', to='pos_system.item')),
            ],
            options={
                'db_table': 'rentals',
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_time', models.DateTimeField()),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tax_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pos_system.employee')),
            ],
            options={
                'db_table': 'sales',
            },
        ),
        migrations.CreateModel(
            name='SaleItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(validators=[MinValueValidator(1)])),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos_system.item')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='pos_system.sale')),
            ],
            options={
                'db_table': 'sale_items',
                'unique_together': {('sale', 'item')},
            },
        ),
        migrations.CreateModel(
            name='ReturnTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_time', models.DateTimeField()),
                ('total_refund', models.DecimalField(decimal_places=2, max_digits=10)),
                ('late_fee_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pos_system.employee')),
            ],
            options={
                'db_table': 'return_transactions',
            },
        ),
        migrations.CreateModel(
            name='ReturnItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(validators=[MinValueValidator(1)])),
                ('days_late', models.IntegerField(default=0)),
                ('late_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos_system.item')),
                ('rental', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos_system.rental')),
                ('return_transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='pos_system.returntransaction')),
            ],
            options={
                'db_table': 'return_items',
            },
        ),
        migrations.CreateModel(
            name='EmployeeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('login', 'Login'), ('logout', 'Logout')], max_length=10)),
                ('timestamp', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='pos_system.employee')),
            ],
            options={
                'db_table': 'employee_logs',
            },
        ),
        migrations.AddIndex(
            model_name='item',
            index=models.Index(fields=['item_id'], name='items_item_id_idx'),
        ),
        migrations.AddIndex(
            model_name='item',
            index=models.Index(fields=['name'], name='items_name_idx'),
        ),
        migrations.AddIndex(
            model_name='customer',
            index=models.Index(fields=['phone_number'], name='customers_phone_number_idx'),
        ),
        migrations.AddIndex(
            model_name='rental',
            index=models.Index(fields=['customer', 'is_returned'], name='rentals_customer_returned_idx'),
        ),
        migrations.AddIndex(
            model_name='rental',
            index=models.Index(fields=['due_date'], name='rentals_due_date_idx'),
        ),
        migrations.AddIndex(
            model_name='rental',
            index=models.Index(fields=['item'], name='rentals_item_idx'),
        ),
        migrations.AddIndex(
            model_name='sale',
            index=models.Index(fields=['transaction_time'], name='sales_transaction_time_idx'),
        ),
        migrations.AddIndex(
            model_name='sale',
            index=models.Index(fields=['employee'], name='sales_employee_idx'),
        ),
        migrations.AddIndex(
            model_name='coupon',
            index=models.Index(fields=['code'], name='coupons_code_idx'),
        ),
        migrations.AddIndex(
            model_name='employeelog',
            index=models.Index(fields=['employee', 'timestamp'], name='employee_logs_employee_timestamp_idx'),
        ),
        migrations.AddIndex(
            model_name='employeelog',
            index=models.Index(fields=['action'], name='employee_logs_action_idx'),
        ),
    ]

