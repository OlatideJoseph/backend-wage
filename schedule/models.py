from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.

class SchedulePayment(models.Model):
    account = models.CharField(max_length=10, unique=True)
    bank_code = models.CharField(max_length=10)
    account_name = models.CharField(max_length=80)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    amount = models.CharField(max_length=7, default='60000',
            help_text='Must greater than 0 and must not have a letter preceded')
    created_on = models.DateTimeField(auto_now=True)
    has_paid = models.BooleanField(default=False)
    pay_date = models.DateTimeField(default=timezone.now)
    

    def __str__(self) -> str:
        return f'Scheduled By {self.created_by.username} for {self.account_name}'

    @classmethod
    def not_paid(cls):
        '''
            Checks if queries all the data of not paid
        '''
        return cls.objects.filter(has_paid=False)

    @classmethod
    def not_paid_today(cls):
        '''
            Filters the not_paid classmethod
            by today
        '''
        return [ins for ins in cls.not_paid() if \
            (ins.pay_date.day == timezone.now().day)
        ]

class TransferRecipient(models.Model):
    recipient_code = models.CharField(max_length=60, unique=True)
    payment = models.OneToOneField(SchedulePayment, on_delete=models.CASCADE, related_name='recipient')

    def __str__(self) -> str:
        return f'Recipient Cose: {self.recipient_code}'

class Transaction(models.Model):
    reference = models.CharField(max_length=40, unique=True)
    recipients = models.ForeignKey(TransferRecipient, on_delete=models.CASCADE, related_name='transactions')
    status = models.TextField()
    created_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f'Transaction {self.refrence} {status}'

class PaidPayment(models.Model):
    date_paid = models.DateTimeField(default=timezone.now)
    schedule_pay = models.ForeignKey(SchedulePayment, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Paid Account:{self.schedule_pay.account} on {self.date_paid}'



class FlutterWaveTransaction(models.Model):
    trsc_id = models.PositiveIntegerField(null=False)
    reference = models.CharField(max_length=80, unique=True)
    payment = models.ForeignKey(SchedulePayment, on_delete=models.CASCADE, related_name='fw_transactions')

    def __str__(self) -> str:
        return 'FW -%d' %(self.trsc_id)

