import json
from datetime import datetime
from django.db.models import Sum
from django.core import serializers
from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from .models import *


## 信用卡操作部分
@require_http_methods(["GET"])
def get_cards(request):
    """
    show all cards, return all credit cards
    """
    response = {}
    try:
        online_user_id = request.GET['online_user_id']
        cards = CreditCard.objects.filter(online_user=Online_user.objects.get(person_id=online_user_id))
        response['status'] = 'success'
        response['message'] = 'Cards show successfully.'
        response['error_num'] = 0
        response['cardlist'] = json.loads(serializers.serialize('json', cards))
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["GET"])
def add_new_card(request):
    """
    create a new card and return the card
    """
    response = {}
    try:
        # Create a new credit card
        online_user_id = request.GET['online_user_id']
        card = CreditCard().newcard(online_user_id)
        # Serialize the card object to JSON format
        card_json = serialize('json', [card], ensure_ascii=False)

        # Prepare the response dictionary
        response['status'] = 'success'
        response['message'] = 'Cards added successfully.'
        response['error_num'] = 0
        response['card'] = card_json

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    # Use JsonResponse to return the response dictionary as JSON
    return JsonResponse(response)


@require_http_methods(["GET"])
def change_password(request):
    """
    Change the password of a credit card and return the card
    """
    response = {}
    try:

        # Fetch the credit card using the account_id from URL parameters
        card = CreditCard.objects.get(account_id=request.GET['account_id'])

        # Get the new password from the parsed data
        new_password = request.GET['new_password']

        # Update the password
        card.modify_password(new_password)
        card.save()

        response['status'] = 'success'
        response['message'] = 'Password has been changed successfully.'
        response['error_num'] = 0
        response['card'] = serialize('json', [card], ensure_ascii=False)

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    # Use JsonResponse to return the response dictionary as JSON
    return JsonResponse(response)


## 账单操作部分
@require_http_methods(["GET"])
def pay_to(request):
    """
    add a record to the transfer_record
    """
    response = {}
    try:
        new_transaction = Transaction(
            account_in_id=request.GET['account_in_id'],
            account_out_id=request.GET['account_out_id'],
            transfer_amount=request.GET['amount'],
            transfer_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 使用当前时间作为交易日期
            # transfer_date=request.GET['date']
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


@require_http_methods(["GET"])
def show_month_bill(request):
    """
    'user' get the bill of 'year''month'
    """
    response = {}
    try:
        year = request.GET['year']
        month = request.GET['month']
        if not year or not month:
            raise ValueError("Year and month parameters are required.")
        bill = Transaction.objects.filter(
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


@require_http_methods(["GET"])
def show_pay_info(request):
    """
    show the detail-information and result of a pay_record (show frontend result)
    """
    response = {}
    try:
        transaction = Transaction.objects.filter(
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


@require_http_methods(["POST"])
def add_new_examiner(request):
    """
    add a new examiner and return the examiner
    """
    response = {}
    sys_manager_id = request.GET['sys_manager_id']
    employee_id = request.GET['employee_id']

    sys_manager = SystemManager.objects.get(sys_manager_id=sys_manager_id)
    try:
        new_examiner = sys_manager.add_credit_examiner(employee_id=employee_id)
        new_examiner_json = serialize('json', [new_examiner], ensure_ascii=False)

        # Prepare the response dictionary
        response['status'] = 'success'
        response['message'] = 'Cards added successfully.'
        response['error_num'] = 0
        response['new_examiner'] = new_examiner_json

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    # Use JsonResponse to return the response dictionary as JSON
    return JsonResponse(response)


@require_http_methods(["GET"])
def get_applications(request):
    """
    show all applications, return all applications
    """
    response = {}
    try:
        applications = CreditCardApplication.objects.filter()
        response['status'] = 'success'
        response['message'] = 'Applications show successfully.'
        response['error_num'] = 0
        response['list'] = json.loads(serializers.serialize('json', applications))
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["GET"])
def new_application(request):
    """
    User applies for a new credit card application, and return the application details.
    """
    response = {}
    try:
        online_user_id = request.GET['online_user_id']

        # Create a new application using the obtained online_user
        application = CreditCardApplication().new_apply(online_user_id)

        response['status'] = 'success'
        response['message'] = 'New application has been created.'
        response['error_num'] = 0
        response['application'] = serialize('json', [application], ensure_ascii=False)

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["GET"])
def get_application_at(request):
    """
    User gets his own application details
    """
    response = {}
    try:
        online_user_id = request.GET['online_user_id']
        applications = CreditCardApplication.objects.filter(online_user_id=online_user_id)

        response['status'] = 'success'
        response['message'] = 'Get applications successfully.'
        response['application_list'] = json.loads(serializers.serialize('json', applications))
        response['error_num'] = 0
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["GET"])
def change_application_state(request):
    """
    Examiner change the state of a credit card application
    """
    response = {}
    try:
        # Fetch the application using the apply_id from URL parameters
        apply = CreditCardApplication.objects.get(apply_id=request.GET['apply_id'])
        # Get the result and examiner_id
        apply_result = request.GET['apply_result']
        examiner_id = request.GET['examiner_id']
        # Update the apply_status and apply_result
        apply.change_state(apply_result, examiner_id)
        apply.save()

        response['status'] = 'success'
        response['message'] = 'The application has been examined.'
        response['error_num'] = 0

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["GET"])
def frozen_card(request):
    response = {}
    try:
        card = CreditCard.objects.get(account_id=request.GET['account_id'])
        card.frozen_card()
        response['status'] = 'success'
        response['message'] = 'New application has been created.'
        response['card'] = serialize('json', [card], ensure_ascii=False)
        response['error_num'] = 0
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["GET"])
def update_limit(request):
    response = {}
    try:
        card = CreditCard.objects.get(account_id=request.GET['account_id'])
        amount = request.GET['amount']
        card.update_credit_limit(amount)
        response['status'] = 'success'
        response['message'] = 'Limit has been updated.'
        response['card'] = serialize('json', [card], ensure_ascii=False)
        response['error_num'] = 0
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


def cancel_card(request):
    response = {}
    try:
        card = CreditCard.objects.get(account_id=request.GET['account_id'])
        card.cancel_card()
        response['status'] = 'success'
        response['message'] = 'Card has been cancelled.'
        response['error_num'] = 0
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


def repay(request):
    response = {}
    try:
        amount = float(request.GET['amount'])
        card = CreditCard.objects.get(account_id=request.GET['account_id'])
        pay_account = int(request.GET['pay_account'])
        card.credit_repay(amount, pay_account)
        response['status'] = 'success'
        response['message'] = 'Payment has been completed.'
        response['card'] = serialize('json', [card], ensure_ascii=False)
        response['error_num'] = 0
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


def lost_card(request):
    response = {}
    try:
        card = CreditCard.objects.get(account_id=request.GET['account_id'])
        card.report_lost()
        response['status'] = 'success'
        response['message'] = 'Card has been reported lost successfully.'
        response['error_num'] = 0
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
