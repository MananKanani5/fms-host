from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('login/', views.user_login, name='login'),
    path('user_logout/', views.user_logout, name='user_logout'),
  

    #admin screen path
    path('admin_dashboard/', views.admin_dashboard, name = 'admin_dashboard'),
    path('students/', views.students, name = 'students'),
    path('student_details/<str:studentId>', views.student_details, name = 'student_details'),
    path('fees_details/', views.fees_details, name = 'fees_details'),
    path('admin_fees_structure/', views.admin_fees_structure, name = 'admin_fees_structure'),
    path('save_fees_structure/<str:feesStructureId>', views.save_fees_structure, name = 'save_fees_structure'),
    path('reports/', views.reports, name = 'reports'),
    path('transaction_receipt/<str:UserId>/<str:FeesTypeId>/<str:transactionId>', views.transaction_receipt, name = 'transaction_receipt'),

    #student screen path
    path('student_dashboard/', views.student_dashboard, name = 'student_dashboard'),
    path('student_fees_structure/', views.student_fees_structure, name = 'student_fees_structure'),
    path('fees_payment/', views.fees_payment, name = 'fees_payment'),
    path('fees_payment_success/', views.fees_payment_success, name = 'fees_payment_success'),
    path('transaction_success/', views.transaction_success, name = 'transaction_success'),
    path('fees_payment_failure/', views.fees_payment_failure, name = 'fees_payment_failure'),
    path('transaction_failure/', views.transaction_failure, name = 'transaction_failure'),
    path('student_fees_structure/', views.student_fees_structure, name = 'student_fees_structure'),
    path('student_transactions/', views.student_transactions, name = 'student_transactions'),
    # path('receipt/', views.receipt, name = 'receipt'),


]
