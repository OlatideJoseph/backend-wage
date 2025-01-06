import secrets
from .utils import initiate_transfer_payment as itp, finalize_transfer as ft
from celery import shared_task
from . import models
from django.core.mail import send_mail
from django.utils import timezone
#celery tasks module/app to work across shared processes

@shared_task
def async_itp(amount, recipient, reference):
    return itp(amount, recipient, reference)

@shared_task
def check_pay_user():
    # in this seperate worker process/task this function
    # it queries all scheduled payment that haven't been paid today
    not_paid_today = models.SchedulePayment.not_paid_today()
    # checks if the current hour matches the scheduled hour
    # or is greater than scheduled hour
    matches = [pay for pay in not_paid_today if \
            pay.pay_date.hour <= timezone.now().hour]
    # initiate a transfer with the transfer recipient relationship
    # of the recipient table
    for pay in matches:
        if pay:
            print('Found a match')
            # transfer ref unique id
            ref = secrets.token_hex(16)
            resp = itp(pay.amount, pay.recipient.recipient_code, ref)
            trans = models.Transaction.objects.\
                    create(reference=ref, recipient=pay.recipient,
                    status=resp['data'].get('status'))
            # Notifies and updates payment if initated transfer is a success
            if (trans.status == 'success'):
                # changes the record to paid
                pay.has_paid = True
                pay.save()
                models.PaidPayment.objects.create(schedule_pay=pay)
                # Notifies the users
                send_mail(
                    f'Scheduled Transfer at {str(pay.pay_date)} success',
                    f'transfer successful for {pay.account_name}',
                    'no-reply@auto-wage-lease.com',
                    [pay.created_by.email]
                )
