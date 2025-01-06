from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreateSchedulePaymentAPIView.as_view(), name='create-schedule'),
    path('bank-resolve/', views.resolve_account, name='resolve-account'),
    path('user-list/', views.ListUserAPIView.as_view(), name='list-user'),
]
