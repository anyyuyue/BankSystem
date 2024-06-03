import json
from datetime import datetime
from django.db.models import Sum
from django.core import serializers
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from .models import *
from django.views.decorators.csrf import csrf_exempt


# 信用卡操作部分---------------------------------------------------------------------------
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


@csrf_exempt
@require_http_methods(["POST"])
def add_new_card(request):
    """
    create a new card and return the card
    """
    response = {}
    try:
        # 解析 JSON 数据
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        online_user_id = body.get('online_user_id')
        card = CreditCard().new_card(online_user_id)

        # Prepare the response dictionary
        response['status'] = 'success'
        response['message'] = 'Cards added successfully.'
        response['error_num'] = 0

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


# 账单操作部分------------------------------------------------------------------------------
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


# 信用卡审核员部分----------------------------------------------------------------------------
@require_http_methods(["POST"])
def add_examiner(request):
    """
    get employee_id, add a new examine, return the examiner
    """
    response = {}
    try:
        new_examiner = CreditCardExaminer.add_credit_examiner(employee_id=request.POST.get['employee_id'])
        new_examiner_json = serialize('json', [new_examiner], ensure_ascii=False)

        # Prepare the response dictionary
        response['status'] = 'success'
        response['message'] = 'Examiner added successfully.'
        response['error_num'] = 0
        response['new_examiner'] = new_examiner_json

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["GET"])
def get_examiners(request):
    """
    show all examiners
    """
    response = {}
    try:
        examiners = CreditCardExaminer.objects.filter()
        response['status'] = 'success'
        response['message'] = 'Examiners show successfully.'
        response['error_num'] = 0
        response['list'] = json.loads(serializers.serialize('json', examiners))
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["POST"])
def modify_examiner(request):
    """
    Modify an existing examiner's information(account & password)
    """
    response = {}
    try:
        # Fetch the examiner using the examiner_id from URL parameters
        examiner = CreditCardExaminer.objects.get(credit_examiner_id=request.POST.get['examiner_id'])
        # Get the new information
        new_account = request.POST.get['new_account']
        new_password = request.POST.get['new_password']

        # Update the password
        examiner.modify_examiner_info(new_account, new_password)
        examiner.save()

        response['status'] = 'success'
        response['message'] = 'Examiner info has been modified successfully.'
        response['error_num'] = 0

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["POST"])
def grant_authority(request):
    """
    Grant an existing examiner the authority to examine
    """
    response = {}
    try:
        # Fetch the examiner using the examiner_id from URL parameters
        examiner = CreditCardExaminer.objects.get(credit_examiner_id=request.POST.get['examiner_id'])
        # Set authority
        examiner.grant()
        examiner.save()

        response['status'] = 'success'
        response['message'] = 'Grant authority successfully.'
        response['error_num'] = 0

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["POST"])
def revoke_authority(request):
    """
    Revoke the authority of an existing examiner
    """
    response = {}
    try:
        # Fetch the examiner using the examiner_id from URL parameters
        examiner = CreditCardExaminer.objects.get(credit_examiner_id=request.POST.get['examiner_id'])
        # Revoke authority
        examiner.revoke()
        examiner.save()

        response['status'] = 'success'
        response['message'] = 'Revoke authority successfully.'
        response['error_num'] = 0

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["POST"])
def delete_examiner(request):
    """
    Delete an existing examiner
    """
    response = {}
    try:
        examiner = CreditCardExaminer.objects.get(credit_examiner_id=request.POST.get('examiner_id'))
        examiner.delete()
        response['status'] = 'success'
        response['message'] = 'Examiner has been deleted successfully.'
        response['error_num'] = 0
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 申请管理部分-----------------------------------------------------------------------------------------
@require_http_methods(["GET"])
def get_check_applications(request):
    """
    show all applications, return all applications
    """
    response = {}
    try:
        applications = CreditCardApplication.objects.filter(apply_status=1)
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
def get_uncheck_applications(request):
    """
    show all applications, return all applications
    """
    response = {}
    try:
        applications = CreditCardApplication.objects.filter(apply_status=0)
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


@csrf_exempt
@require_http_methods(["POST"])
def change_application_state(request):
    """
    Examiner change the state of a credit card application
    """
    response = {}
    try:
        # 解析 JSON 数据
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        apply_id = body.get('apply_id')
        # print(f"Received apply_id: {apply_id}")  # 调试输出

        if not apply_id:
            raise ValueError("apply_id is required")

        # 确保 apply_id 转换为整数
        apply_id = int(apply_id)
        apply = CreditCardApplication.objects.get(apply_id=apply_id)

        # Get the result and examiner_id
        apply_result = body.get('apply_result')
        examiner_id = body.get('examiner_id')

        if not apply_result or not examiner_id:
            raise ValueError("apply_result and examiner_id are required")

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
