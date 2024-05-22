import json

from django.core import serializers
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from creditcard.models import *


# pay_to: add a record to the transfer_record
@require_http_methods(["GET"])
def pay_to(request):
    response = {}
    try:
        new_transaction = transfer_record(
            account_in_id=request.GET['account_in_id'],
            account_out_id=request.GET['account_out_id'],
            transfer_amount=request.GET['amount'],
            transfer_date=request.GET['date']
        )
        new_transaction.save()
        response['status'] = 'success'
        response['message'] = 'New transaction has been created and saved successfully.'
        response['error_num'] = 0
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


# show_month_bill: 'user' get the bill of 'year''month'
@require_http_methods(["GET"])
def show_month_bill(request):
    response = {}
    try:
        year = request.GET['year']
        month = request.GET['month']
        if not year or not month:
            raise ValueError("Year and month parameters are required.")
        bill = transfer_record.objects.filter(
            account_in_id=request.GET['account_in_id'],
            transfer_date__year=year,
            transfer_date__month=month
        )
        response['total_amount'] = bill.aggregate(total=Sum('transfer_amount'))['total'] or 0
        response['list'] = json.loads(serializers.serialize('json', bill))
        response['status'] = 'success'
        response['message'] = 'All bills have been saved.'
        response['error_num'] = 0
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


# show_pay: show the detail-information and result of a pay_record (show frontend result)
@require_http_methods(["GET"])
def show_pay_info(request):
    response = {}
    try:
        transaction = transfer_record.objects.filter(
            transfer_record_id=request.GET['transfer_record_id'],
        )
        response['list'] = json.loads(serializers.serialize('json', transaction))
        response['status'] = 'success'
        response['message'] = 'All payment infos have been saved.'
        response['error_num'] = 0
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)
