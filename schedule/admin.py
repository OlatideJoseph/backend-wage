from django.contrib import admin
from .models import SchedulePayment, TransferRecipient,Transaction, PaidPayment
# Register your models here.

admin.site.register(SchedulePayment)
admin.site.register(TransferRecipient)
admin.site.register(Transaction)
admin.site.register(PaidPayment)

