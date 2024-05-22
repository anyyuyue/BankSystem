from django.urls import path, re_path
from creditcard import views

urlpatterns = [
    re_path('pay_to', views.pay_to),
    re_path('show_month_bill', views.show_month_bill),
]
