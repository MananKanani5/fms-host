from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class StudentDetail(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    
    UserId = models.CharField(max_length=20)
    Name = models.CharField(max_length=50)
    Gender = models.CharField(max_length=10)
    DOB = models.DateField(max_length=20)
    Email = models.EmailField(max_length=20)
    Mobile = models.CharField(max_length=50)
    Address = models.CharField(max_length=100)
    Religion = models.CharField(max_length=10)
    Caste = models.CharField(max_length=20)
    CasteCategory = models.CharField(max_length=20)
    Course = models.CharField(max_length=20)
    Department = models.CharField(max_length=50)
    CourseYear = models.CharField(max_length=20)
    AcademicYear = models.CharField(max_length=10)
    FeesTypeId = models.IntegerField(default=None, blank=True, null=True)
    TotalFees = models.IntegerField()
    RemainingFees = models.IntegerField()
    PaidFees = models.IntegerField()
    FeesStatus = models.CharField(max_length=10)
    LastLogin = models.DateTimeField(max_length=50)
    


class TransactionDetail(models.Model):
    UserId = models.CharField(max_length=20)
    TransactionId = models.CharField(max_length=50)
    TransactionTypeId = models.IntegerField(default=0)
    FeesTypeId = models.IntegerField(default=0)
    Amount = models.IntegerField()
    DateTime = models.DateTimeField(max_length=50)
    Method = models.CharField(max_length=50)
    Status = models.CharField(max_length=50)


class FeesDetail(models.Model):
    TypeId = models.IntegerField()
    Type = models.CharField(max_length=50)
    TutionFees = models.IntegerField()
    DevelopmentFees = models.IntegerField()
    OtherFees = models.IntegerField()
    ExamFees = models.IntegerField()
    DepositAndCautionMoney = models.IntegerField()
    StudentInsurance = models.IntegerField()
    AlumniAssociationLifeMembershipFees = models.IntegerField()
    ConvocationFees = models.IntegerField(default=0)
    Contingency = models.IntegerField(default=0)
    TotalFee = models.IntegerField()


