from django.urls import path

from . import views

urlpatterns = [

    path('get_cards', views.get_cards),  # 显示用户的所有卡
    path('new_application', views.new_application),
    path('get_application_at', views.get_application_at),  # 用户查看自己的申请
    path('change_password', views.change_password),
    path('frozen_card', views.frozen_card),
    path('pay_to', views.pay_to),
    path('show_month_bill', views.show_month_bill),
    path('update_limit', views.update_limit),
    path('cancel_card', views.cancel_card),
    path('repay', views.repay),


    path('add_new_card', views.addnewcard),
    path('get_applications', views.get_applications),  # 审核员看
    path('change_application_state', views.change_application_state),

    path('add_examiner', views.add_examiner),
    path('get_examiners', views.get_examiners),
    path('change_examiner', views.change_examiner),
    path('grant_authority', views.grant_authority),
    path('revoke_authority', views.revoke_authority),


]