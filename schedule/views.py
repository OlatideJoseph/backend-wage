from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, decorators, response, views, permissions
from . import models
from . import utils
from . import serializers
# Create your views here.

class CreateSchedulePaymentAPIView(generics.CreateAPIView):
    serializer_class = serializers.SchedulePaymentSerializer
    queryset = models.SchedulePayment.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ListUserAPIView(generics.ListAPIView):
    '''
        The lists all user view
    '''
    serializer_class = serializers.UserListSerializer
    queryset = get_user_model().objects.all()

@decorators.api_view(['GET'])
def resolve_account(request):
    '''
    account_number -- Resolve Account Number
    bank_code -- Resolve Bank Code
    '''
    serializer = serializers.BankResolveSerializer(data=request.GET)
    serializer.is_valid(raise_exception=True)
    accn = serializer.validated_data.get('account_number')
    bank_code = serializer.validated_data.get('bank_code')

    return response.Response(utils.resolve_account(accn, bank_code))
