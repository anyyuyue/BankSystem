import json

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from creditcard.models import CreditCard


# Create your views here.
@require_http_methods(["GET"])
def add_card(request):
    response = {}
    try:
        creditcard = CreditCard(account_id=request.GET['account_id'])
        creditcard.save()
        response['status'] = 'success'
        response['message'] = 'Credit card has been saved.'
        response['error_num'] = 0
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["GET"])
def show_cards(request):
    response = {}
    try:
        creditcards = CreditCard.objects.filter()
        response['list'] = json.loads(serializers.serialize('json', creditcards))
        response['status'] = 'success'
        response['message'] = 'All cards have been saved.'
        response['error_num'] = 0
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)