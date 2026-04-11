from django.urls import path
from .views import *

urlpatterns = [
    path('customers/', customer_list),
    path('add/', add_customer),
    path('measurements/',measurement_list),
    path('customer/<int:id>/', customer_detail),
    path('orders/', order_list),
    path('pending-orders/', pending_orders),
    path('ready-orders/', ready_orders),
    path('dashboard/', dashboard),
    path('customer-orders/<int:customer_id>/', customer_orders),
    path('add-order/', add_order),
    path('edit-order/<int:order_id>/', edit_order),
    path('delete-order/<int:order_id>/', delete_order),
    path('today-deliveries/', today_deliveries),
    path('customer-measurements/<int:customer_id>/', customer_measurements),
    path('edit-measurement/<int:measurement_id>/', edit_measurement),
    path('delete-customer/<int:customer_id>/', delete_customer),
    path('history/', history_list),
    path('',home,name='home'),
    path('mark-paid/<int:id>/', mark_paid),


]

