from django.contrib import admin
from fms_app.models import *

class FMSStudentDetails(admin.ModelAdmin):
    list_display = ('UserId','Name','Gender','DOB','Email',
                    'Mobile','Address','Religion','Caste','CasteCategory',
                    'Course','Department','CourseYear','AcademicYear','FeesTypeId','TotalFees',
                    'RemainingFees','PaidFees','FeesStatus','LastLogin')

class FMSTransactionDetails(admin.ModelAdmin):
    list_display = ('UserId','TransactionId','TransactionTypeId','FeesTypeId','Amount','DateTime','Method','Status')

class FMSFeesDetails(admin.ModelAdmin):
    list_display = ('TypeId','Type','TutionFees','DevelopmentFees','OtherFees',
                    'ExamFees','DepositAndCautionMoney','StudentInsurance',
                    'AlumniAssociationLifeMembershipFees','ConvocationFees','Contingency','TotalFee')

# Register your models here.
admin.site.register(StudentDetail,FMSStudentDetails)
admin.site.register(TransactionDetail,FMSTransactionDetails)
admin.site.register(FeesDetail,FMSFeesDetails)
