from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from fms_app.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator 
from django.conf import settings
import razorpay
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime

# Create your views here.

def user_login(request): 
    if request.method == "POST":
        username = request.POST["ID"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            messages.success(request, 'There was Error in Logging In, Try Again...')
            return redirect('login')
    else:
        return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')        

#admin views
@login_required
def admin_dashboard(request):
    return render(request, 'admin_ui/admin_dashboard.html')

@login_required
def students(request):
    items_per_page = 10
    
    if request.method == "POST":
        searchTerm = request.POST.get("searchTerm")
        studentData = StudentDetail.objects.filter(Q(UserId__contains=searchTerm) | Q(Name__contains=searchTerm))
    else:
        studentData = StudentDetail.objects.all()

    paginator = Paginator(studentData, items_per_page)
    
    page = request.GET.get('page')
    studentData = paginator.get_page(page)
    max_pages_to_show = 3
    start_page = max(1, studentData.number - (max_pages_to_show // 2))
    end_page = min(studentData.paginator.num_pages, start_page + max_pages_to_show - 1)
    page_range = range(start_page, end_page + 1)

    return render(request, 'admin_ui/students.html', {'studentData': studentData, 'page_range': page_range})

@login_required
def student_details(request, studentId):
    changed = False
    if request.method == "POST":
        StudentDetail.objects.filter(UserId=studentId).update(TotalFees = request.POST.get('totalFees'), 
                                                              RemainingFees = request.POST.get('remainingFees'), 
                                                              PaidFees = request.POST.get('paidFees'))
        changed = True

    studentData =  StudentDetail.objects.filter(UserId = studentId)
    return render(request, 'admin_ui/student_details.html',{'studentData':studentData,'changed':changed})

@login_required
def transaction_receipt(request, UserId, FeesTypeId, transactionId):
    studentData =  StudentDetail.objects.filter(UserId = UserId)  
    feesData = FeesDetail.objects.filter(TypeId = FeesTypeId) 
    transactionData = TransactionDetail.objects.filter(TransactionId = transactionId)  
    return render(request, 'transaction_receipt.html',{ 'studentData':studentData, 'feesData':feesData, 'transactionData': transactionData})
    # return render(request, 'receipt.html')


@login_required
def fees_details(request):
    return render(request, 'admin_ui/fees_details.html')

@login_required
def admin_fees_structure(request):
    if request.method == "POST":
        feesStructureId = request.POST["feesID"]
        print(feesStructureId)
        feesData = FeesDetail.objects.filter(TypeId = feesStructureId)   
        return render(request, 'admin_ui/fees_structure.html',{'feesData':feesData})
    
    return

@login_required
def save_fees_structure(request, feesStructureId):
    changed = False
    if request.method == "POST":
        FeesDetail.objects.filter(TypeId=feesStructureId).update(
            TutionFees = request.POST.get('TutionFees'), 
            DevelopmentFees = request.POST.get('DevelopmentFees'), 
            OtherFees = request.POST.get('OtherFees'),
            ExamFees = request.POST.get('ExamFees'),
            DepositAndCautionMoney = request.POST.get('DepositAndCautionMoney'),
            StudentInsurance = request.POST.get('StudentInsurance'),
            AlumniAssociationLifeMembershipFees = request.POST.get('AlumniAssociationLifeMembershipFees'),
            ConvocationFees = request.POST.get('ConvocationFees'),
            Contingency = request.POST.get('Contingency'),
            TotalFee = request.POST.get('TotalFee')
        )
        changed = True
        print(changed)
    
    feesData = FeesDetail.objects.filter(TypeId = feesStructureId)   
    return render(request, 'admin_ui/fees_structure.html',{'feesData':feesData,'changed':changed})

@login_required
def reports(request):
    items_per_page = 10
    
    if request.method == "POST":
        searchTerm = request.POST.get("searchTerm")
        feesData = TransactionDetail.objects.filter(Q(UserId__contains=searchTerm) | Q(TransactionId__contains=searchTerm))
    else:
        feesData = TransactionDetail.objects.all()

    paginator = Paginator(feesData, items_per_page)
    
    page = request.GET.get('page')
    feesData = paginator.get_page(page)
    max_pages_to_show = 3
    start_page = max(1, feesData.number - (max_pages_to_show // 2))
    end_page = min(feesData.paginator.num_pages, start_page + max_pages_to_show - 1)
    page_range = range(start_page, end_page + 1)

    return render(request, 'admin_ui/reports.html', {'feesData': feesData, 'page_range': page_range})


#student views

@login_required
def student_dashboard(request):
    return render(request, 'student_ui/student_dashboard.html')

@login_required
def student_fees_structure(request):
    feesData = FeesDetail.objects.filter(TypeId = request.user.studentdetail.FeesTypeId)   
    return render(request, 'student_ui/fees_structure.html',{'feesData':feesData})

# FOR  RECEIPT
# @login_required
# def receipt(request):
#     transactionData = TransactionDetail.objects.filter(UserId = request.user)  
#     feesData = FeesDetail.objects.filter(TypeId = request.user.studentdetail.FeesTypeId)   
#     return render(request, 'student_ui/receipt.html',{'feesData':feesData, 'transactionData': transactionData})

@login_required
def fees_payment(request):
    if request.method == "POST":
        # name = request.POST["name"]
        amount = int(request.POST["feesID"]) * 100
        client = razorpay.Client(auth =(settings.RAZOR_KEY_ID , settings.RAZOR_KEY_SECRET))
        razorpay_order = client.order.create({'amount':amount, 'currency':'INR', 'payment_capture':'1' })
        
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
    
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount / 100
        context['currency'] = "INR"

        return render(request, 'student_ui/fees_payment.html', context=context)
    
    return render(request, 'student_ui/fees_payment.html')


@login_required
def student_transactions(request):
    transactionData = TransactionDetail.objects.filter(UserId = request.user)   
    return render(request, 'student_ui/student_transactions.html',{'transactionData':transactionData})

@login_required
def fees_payment_success(request):
    response_data = request.GET.get('response')
    if response_data:
        response = json.loads(response_data)

        feesStatus = ""
        if response['RemainingFees'] == 0:
            feesStatus = "Paid"
        else:
            feesStatus = "Partial"

        StudentDetail.objects.filter(UserId=request.user).update(RemainingFees = response['RemainingFees'], 
                                                              PaidFees = response['PaidFees'],FeesStatus = feesStatus )
        transactionRow = TransactionDetail(UserId=request.user, TransactionId=response['razorpay_payment_id'],
                                           TransactionTypeId=response['TransactionTypeId'], FeesTypeId=request.user.studentdetail.FeesTypeId, Amount=response['Amount'],
                                           DateTime=datetime.now(), Method=response['Method'], Status="Success")
        transactionRow.save()
    return redirect('transaction_success')

#we are using this one extra function to hide the data exposed while calling transactionSuccess function from JS script after transaction.
def transaction_success(request):
    return render(request, 'student_ui/fees_payment.html', {'changed': True})

@login_required
def fees_payment_failure(request):
    response_data = request.GET.get('response')
    if response_data:
        response = json.loads(response_data)
        transactionRow = TransactionDetail(UserId=request.user, TransactionId=response['razorpay_payment_id'],
                                           TransactionTypeId=response['TransactionTypeId'], FeesTypeId=request.user.studentdetail.FeesTypeId, Amount=response['Amount'],
                                           DateTime=datetime.now(), Method=response['Method'], Status="Failure")
        transactionRow.save()
    return redirect('transaction_failure')

#we are using this one extra function to hide the data exposed while calling transactionSuccess function from JS script after transaction.
def transaction_failure(request):
    return render(request, 'student_ui/fees_payment.html', {'changed': True})



