import json
import pytz
from django.db.models import Sum
from django.core import serializers
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import make_aware
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
        online_user_id = request.GET.get('online_user_id')
        if not online_user_id:
            raise ValueError("online_user_id is required")
        cards = CreditCard.objects.filter(online_user=Online_user.objects.get(person_id=online_user_id))
        response['status'] = 'success'
        response['message'] = 'Cards show successfully.'
        response['error_num'] = 0
        response['list'] = json.loads(serializers.serialize('json', cards))
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
        CreditCard().new_card(online_user_id)

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


@csrf_exempt
@require_http_methods(["POST"])
def frozen_card(request):
    response = {}
    try:
        # 解析 JSON 数据
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        account_id = body.get('account_id')
        if not account_id:
            raise ValueError("account_id is required")
        password = body.get('password')
        if not password:
            raise ValueError("password is required")
        card = CreditCard.objects.get(account_id=account_id)
        card.frozen_card(password)

        response['status'] = 'success'
        response['message'] = 'New application has been created.'
        response['error_num'] = 0
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def update_limit(request):
    response = {}
    try:
        # 解析 JSON 数据
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        account_id = body.get('account_id')
        if not account_id:
            raise ValueError("account_id is required")
        amount = body.get('amount')
        if not amount:
            raise ValueError("amount is required")
        password = body.get('password')
        if not password:
            raise ValueError("password is required")
        card = CreditCard.objects.get(account_id=account_id)
        card.update_credit_limit(password, amount)
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


@csrf_exempt
@require_http_methods(["POST"])
def repay(request):
    response = {}
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        account_id = body.get('account_id')
        pay_account = body.get('pay_account')
        pay_password = body.get('pay_password')
        amount = body.get('amount')
        print(account_id, pay_account, pay_password, amount)

        pay_card = CreditCard.objects.get(account_id=pay_account)
        repay_card = CreditCard.objects.get(account_id=account_id)
        pay_card.transfer_out(amount, pay_password)
        repay_card.transfer_in(amount)

        response['status'] = 'success'
        response['message'] = 'Payment has been completed.'
        response['error_num'] = 0
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def lost_card(request):
    response = {}
    try:
        # 解析 JSON 数据
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        account_id = body.get('account_id')
        if not account_id:
            raise ValueError("account_id is required")
        password = body.get('password')
        if not password:
            raise ValueError("password is required")
        card = CreditCard.objects.get(account_id=account_id)
        card.report_lost(password)
        response['status'] = 'success'
        response['message'] = 'Card has been reported lost successfully.'
        response['error_num'] = 0
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 账单操作部分------------------------------------------------------------------------------
@csrf_exempt
@require_http_methods(["POST"])
def pay_to(request):
    """
    add a record to the transfer_record
    """
    response = {}
    try:
        # 解析json
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        account_in_id = body.get('account_in_id')
        account_out_id = body.get('account_out_id')
        amount = float(body.get('amount'))
        password = body.get('password')

        # update the balance of payer and receiver
        in_card = CreditCard.objects.get(account_id=account_in_id)
        out_card = CreditCard.objects.get(account_id=account_out_id)
        in_card.transfer_in(amount)
        out_card.transfer_out(amount, password)

        # update the information in transaction
        new_transaction = Transaction(
            account_in_id=body.get('account_in_id'),
            account_out_id=body.get('account_out_id'),
            transfer_amount=body.get('amount'),
            transfer_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 使用当前时间作为交易日期
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


# @require_http_methods(["GET"])
# def show_month_bill(request):
#     response = {}
#     try:
#         year = request.GET['year']
#         month = request.GET['month']
#         if not year or not month:
#             raise ValueError("请输入年月")  # Year and month parameters are required.
#
#         # Ensuring the account_id is provided
#         account_id = request.GET.get('account_id')
#         if not account_id:
#             raise ValueError("请输入要查询的账号")  # Account ID is required.
#
#         # Convert dates to the local timezone
#         local_tz = timezone.get_default_timezone()
#
#         in_bill = Transaction.objects.filter(
#             account_in_id=account_id,
#             transfer_date__year=year,
#             transfer_date__month=month
#         ).annotate(
#             local_date=ExpressionWrapper(F('transfer_date'), output_field=DateTimeField())
#         ).filter(
#             local_date__year=year,
#             local_date__month=month
#         )
#
#         out_bill = Transaction.objects.filter(
#             account_out_id=account_id,
#             transfer_date__year=year,
#             transfer_date__month=month
#         ).annotate(
#             local_date=ExpressionWrapper(F('transfer_date'), output_field=DateTimeField())
#         ).filter(
#             local_date__year=year,
#             local_date__month=month
#         )
#
#         in_total_amount = in_bill.aggregate(Sum('transfer_amount'))['transfer_amount__sum'] or 0
#         out_total_amount = out_bill.aggregate(Sum('transfer_amount'))['transfer_amount__sum'] or 0
#
#         bill = list(chain(in_bill, out_bill))
#         response['total_amount'] = in_total_amount - out_total_amount
#         response['in_amount'] = in_total_amount
#         response['out_amount'] = out_total_amount
#         response['list'] = json.loads(serializers.serialize('json', bill))
#         response['status'] = 'success'
#         response['message'] = 'All bills have been saved.'
#         response['error_num'] = 0
#     except Exception as e:
#         response['status'] = 'error'
#         response['message'] = str(e)
#         response['error_num'] = 1
#
#     return JsonResponse(response)



@require_http_methods(["GET"])
def show_month_bill(request):
    response = {}
    try:
        year = request.GET.get('year')
        month = request.GET.get('month')
        account_id = request.GET.get('account_id')
        if not year or not month:
            raise ValueError("请输入年月")  # Year and month parameters are required.

        # Define your timezone (Asia/Shanghai)
        tz = pytz.timezone('Asia/Shanghai')

        # Create timezone-aware start and end dates
        start_date = datetime(int(year), int(month), 1)
        if month == '12':
            end_date = datetime(int(year) + 1, 1, 1)
        else:
            end_date = datetime(int(year), int(month) + 1, 1)

        start_date = make_aware(start_date, timezone=tz)
        end_date = make_aware(end_date, timezone=tz)

        in_bill = Transaction.objects.filter(
            account_in_id=account_id,
            transfer_date__gte=start_date,
            transfer_date__lt=end_date
        )
        out_bill = Transaction.objects.filter(
            account_out_id=account_id,
            transfer_date__gte=start_date,
            transfer_date__lt=end_date
        )

        # Calculate total in and out amounts
        in_total_amount = in_bill.aggregate(Sum('transfer_amount'))['transfer_amount__sum'] or 0
        out_total_amount = out_bill.aggregate(Sum('transfer_amount'))['transfer_amount__sum'] or 0

        # Prepare bills list for custom formatting
        bills = list(in_bill) + list(out_bill)
        formatted_bills = []
        for bill in bills:
            formatted_bills.append({
                'transfer_record_id': bill.transfer_record_id,
                'account_in_id': bill.account_in_id,
                'account_out_id': bill.account_out_id,
                'transfer_amount': bill.transfer_amount,
                'transfer_date': bill.transfer_date.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S')
            })

        # Response setup
        response['total_amount'] = in_total_amount - out_total_amount
        response['in_amount'] = in_total_amount
        response['out_amount'] = out_total_amount
        response['list'] = formatted_bills
        # response['list'] = json.loads(serializers.serialize('json', formatted_bills))
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
@csrf_exempt
@require_http_methods(["POST"])
def add_examiner(request):
    """
    get employee_id, add a new examine, return the examiner
    """
    response = {}
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        employee_id = body.get('employee_id')
        new_examiner = CreditCardExaminer.add_credit_examiner(employee_id)

        # Prepare the response dictionary
        response['status'] = 'success'
        response['message'] = 'Examiner added successfully.'
        response['error_num'] = 0

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


@csrf_exempt
@require_http_methods(["POST"])
def modify_examiner(request):
    """
    Modify an existing examiner's information(account & password)
    """
    response = {}
    try:
        # Fetch the examiner using the examiner_id from URL parameters
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        examiner_id = int(body.get('examiner_id'))
        examiner = CreditCardExaminer.objects.get(credit_examiner_id=examiner_id)
        # Get the new information
        new_account = body.get('new_account')
        new_password = body.get('new_password')

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


@csrf_exempt
@require_http_methods(["POST"])
def grant_authority(request):
    """
    Grant an existing examiner the authority to examine
    """
    response = {}
    try:
        # Fetch the examiner using the examiner_id from URL parameters
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        examiner_id = int(body.get('examiner_id'))
        examiner = CreditCardExaminer.objects.get(credit_examiner_id=examiner_id)
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


@csrf_exempt
@require_http_methods(["POST"])
def revoke_authority(request):
    """
    Revoke the authority of an existing examiner
    """
    response = {}
    try:
        # Fetch the examiner using the examiner_id from URL parameters
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        examiner_id = int(body.get('examiner_id'))
        examiner = CreditCardExaminer.objects.get(credit_examiner_id=examiner_id)
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


@csrf_exempt
@require_http_methods(["POST"])
def delete_examiner(request):
    """
    Delete an existing examiner
    """
    response = {}
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        examiner_id = int(body.get('examiner_id'))
        examiner = CreditCardExaminer.objects.get(credit_examiner_id=examiner_id)
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
