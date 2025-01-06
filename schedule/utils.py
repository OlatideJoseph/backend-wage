import json
import secrets
import requests
from django.conf import settings
from .models import TransferRecipient, Transaction

paystack_url = 'https://api.paystack.co/'

def initiate_transfer_payment(amount: str, recipient: str, reference: str) -> dict:
    '''
        This initiate a transfer for the account and can be queried later
        based on status, but it won't work since
        paystack only allows transfer for registered business
    '''
    data = {
        'source': 'balance',
        'account_number': amount,
        'bank_code': recipient,
        'account_name': reference,
        'reason': 'test program'
    }
    resp = requests.post(f'{paystack_url}/transfer?currency=NGN', data=json.dumps(data), headers={
        'Authorization': f'Bearer {settings.PAYSTACK_API}'
    })
    return resp.json()


def resolve_account(account_number: str, bank_code: str) -> dict:
    resp = requests.get(f'{paystack_url}/bank/resolve?account_number={account_number}&bank_code={bank_code}', headers={
        'Authorization': f'Bearer {settings.PAYSTACK_API}'
    })
    return resp.json()


def finalize_transfer(trf_ref: str) -> dict:
    '''
        Only necessary for account thats turns otp for transfer
        finalize a dummy ref and returns a transfer response
    '''

    return {'status': 'success'}

def create_transfer_recipient(account_number: str, bank_code: str, account_name: str):
    '''
       Creates the Transfer recoipients so that transfer can be 
       initiated.
    '''
    data = {
        'type': 'nuban',
        'account_number': account_number,
        'bank_code': bank_code,
        'name': account_name,
        'currency': 'NGN'
    }
    resp = requests.post(f'{paystack_url}/transferrecipient',
            data=json.dumps(data),
            headers={'Authorization': f'Bearer {settings.PAYSTACK_API}'})
    return resp.json()

# Flutter Wave But Won't
# BASE_URL = "https://api.flutterwave.com/v3/" #v3 api url
# HEADERS = {
#     'Authorization': f'Bearer {settings.FLUTTERWAVE_SK}',
# }
# def get_flutterwave_banks(country: str='NG') -> dict:
#     '''
#        Gets flutterwave available banks
#     '''
#     resp = requests.get(
#         f'{BASE_URL}banks/{country}',
#         headers=HEADERS
#     )# MAKES A GET REQUEST TO FLUTTER API
#     # Automatically json received to dict type
#     return resp.json()


# # transfer fw
# def intiate_flutterwave_transfer(
#         bank_code: str, account_number: int,
#         amount: str, refrence: str
#     ) -> dict:
#     data = {
#         'currency': 'NGN',
#         'narration': 'Scheduled Payment',
#         'debit_currency': 'NGN',
#         'amount': amount,
#         'account_bank': bank_code,
#         'account_number': account_number,

#     }
#     resp = requests.post(
#         f'{BASE_URL}transfers/',
#         data=json.dumps(data)
#         ,
#         headers=HEADERS
#     )
#     return resp.json()
