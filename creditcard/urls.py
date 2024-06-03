from django.urls import path

from . import views

urlpatterns = [

    path('get_cards', views.get_cards),
    # 显示用户的所有卡 http://127.0.0.1:8000/api/get_cards?online_user_id=1
    path('new_application', views.new_application),
    # 用户申请信用卡 http://127.0.0.1:8000/api/new_application?online_user_id=1
    path('get_application_at', views.get_application_at),
    # 用户查看自己的信用卡申请 http://127.0.0.1:8000/api/get_application_at?online_user_id=1
    path('change_password', views.change_password),
    # 用户更改新密码 http://127.0.0.1:8000/api/change_password?account_id=1&new_password=123456
    path('frozen_card', views.frozen_card),
    # 用户冻结卡 http://127.0.0.1:8000/api/frozen_card?account_id=1
    path('pay_to', views.pay_to),
    # 用户支付 http://127.0.0.1:8000/api/pay_to?account_in_id=1&account_out_id=2&amount=1000
    path('show_month_bill', views.show_month_bill),
    # 用户查看月账单 http://127.0.0.1:8000/api/show_month_bill?account_in_id=1&year=2024&month=5
    path('update_limit', views.update_limit),
    # 用户更新信用卡余额 http://127.0.0.1:8000/api/update_limit?account_id=1&amount=2000
    path('cancel_card', views.cancel_card),
    # 用户取消卡 http://127.0.0.1:8000/api/cancel_card?account_id=1
    path('repay', views.repay),
    # 用户还款，要先把balance变成正的才能成功 或者用别的银行卡还款
    # http://127.0.0.1:8000/api/repay?account_id=2&amount=200
    # http://127.0.0.1:8000/api/repay?account_id=2&amount=200&pay_account=3
    path('lost_card', views.lost_card),
    # 挂失卡 http://127.0.0.1:8000/api/lost_card?account_id=1


    path('add_new_card', views.add_new_card),
    # 审核员新建卡 http://127.0.0.1:8000/api/add_new_card?online_user_id=1
    path('get_check_applications', views.get_check_applications),  # 审核员看
    # 显示所有的申请 http://127.0.0.1:8000/api/get_check_applications
    path('get_uncheck_applications', views.get_uncheck_applications),  # 审核员看
    # 显示所有的申请 http://127.0.0.1:8000/api/get_uncheck_applications
    path('change_application_state', views.change_application_state),
    # 审核申请 http://127.0.0.1:8000/api/change_application_state?examiner_id=1&apply_id=1&apply_result=1

    path('add_examiner', views.add_examiner),
    # 添加信用卡审查员 http://127.0.0.1:8000/api/add_examiner?employee_id=1
    path('get_examiners', views.get_examiners),
    # 显示所有的审查员 http://127.0.0.1:8000/api/get_examiners
    path('modify_examiner', views.modify_examiner),
    # 修改信用卡审查员信息 http://127.0.0.1:8000/api/modify_examiner?examiner_id=1&new_account=666&new_password=888
    path('grant_authority', views.grant_authority),
    # 授予权限 http://127.0.0.1:8000/api/grant_authority?examiner_id=1
    path('revoke_authority', views.revoke_authority),
    # 收回权限 http://127.0.0.1:8000/api/revoke_authority?examiner_id=1
    path('delete_examiner', views.delete_examiner),
    # 删除信用卡审查员 http://127.0.0.1:8000/api/delete_examiner?examiner_id=1

]