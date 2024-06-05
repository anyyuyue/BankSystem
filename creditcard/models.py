from datetime import datetime

from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


# 所有职员（应该在其他模块中定义，这里先定义一下方便测试使用）
class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    employee_name = models.CharField(max_length=20, default='name')
    identity_card = models.CharField(max_length=18, default='000000000000000000')


# 信用卡审查员
class CreditCardExaminer(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    credit_examiner_id = models.AutoField(primary_key=True)
    check_authority = models.BooleanField(default=False)
    account = models.CharField(max_length=30, default='000000')
    password = models.CharField(max_length=20, default='password')

    def add_credit_examiner(employee_id):
        try:
            employee = Employee.objects.get(employee_id=employee_id)
            if CreditCardExaminer.objects.filter(employee=employee).exists():
                raise ValueError("This employee is already a creditcard examiner.")

            # create a new CreditCardExaminer
            new_examiner = CreditCardExaminer(
                employee=employee,
                account=employee.identity_card,  # Example account name generation
                password='password',
                check_authority=1  # default grant the authority
            )
            new_examiner.save()
            return new_examiner

        except ObjectDoesNotExist:
            raise ValueError("No such employee exists.")

    def modify_examiner_info(self, new_account, new_password):
        """更改审核员账号信息"""
        # new account is same as others account, not allow
        if not self.account == new_account and CreditCardExaminer.objects.filter(account=new_account).exists():
            raise ValueError("This account already exists.")
        else:
            self.account = new_account
        # new password is the same as the old one, not allow
        if self.password == new_password:
            raise ValueError("New password is the same as the old one")
        else:
            self.password = new_password
            self.save()

    def grant(self):
        if self.check_authority:
            raise ValueError("This account is authorized, can't grant it.")
        else:
            self.check_authority = True

    def revoke(self):
        if not self.check_authority:
            raise ValueError("This account is not authorized, can't revoke it.")
        else:
            self.check_authority = False


class Online_user(models.Model):
    person_id = models.AutoField(primary_key=True)
    identity_card = models.CharField(max_length=18, default='000000000000000000')


# 信用卡模型
class CreditCard(models.Model):
    objects = None
    account_id = models.AutoField(primary_key=True)  # 使用AutoField自动ID
    password = models.CharField(max_length=20, default='password')  # 设置默认密码
    card_type = models.CharField(max_length=10, default='credit')
    online_user = models.ForeignKey(Online_user, on_delete=models.CASCADE, default=None)
    credit_limit = models.FloatField(default=1000.0)  # 信用额度
    balance = models.FloatField(default=0.0)  # 待偿还的金额
    is_frozen = models.BooleanField(default=False)
    is_lost = models.BooleanField(default=False)
    due_date = models.DateTimeField(default=timezone.now)  # Automatically set to today's date as default

    DEFAULT_CREDIT_LIMIT = 1000.0  # 默认信用额度

    @staticmethod
    def new_card(online_user_id):
        ## 需要加上更具不同的信用额度来判断
        new_card = CreditCard()
        new_card.online_user = Online_user.objects.get(person_id=online_user_id)
        new_card.save()
        return new_card

    def modify_password(self, new_password):
        """更改信用卡密码，输入新密码"""
        if not self.password == new_password:
            self.password = new_password
            self.save()
        else:
            raise ValueError("New password is the same as the old one")

    def report_lost(self, password):
        """挂失信用卡，并自动冻结卡"""
        if password != self.password:
            raise ValueError("密码不匹配")
        elif self.is_lost:
            raise ValueError("此卡已挂失")
        elif self.is_frozen:
            raise ValueError("此卡已冻结")
        else:
            self.is_lost = True
            self.is_frozen = True
            self.save()
            return True

    def cancel_card(self):
        """取消信用卡，删除记录"""
        self.delete()
        return True

    def update_credit_limit(self, password, amount):
        """更新信用额度"""
        if password != self.password:
            raise ValueError("密码不匹配")
        elif self.is_lost or self.is_frozen:
            raise ValueError("Can't change credit limit since it's lost or frozen.")
        else:
            self.credit_limit = amount
            self.save()
            return True

    # def credit_repay(self, amount, pay_account_id):
    #     """还款，输入还款金额"""
    #     if amount < 0.0:
    #         raise ValueError("Amount cannot be negative.")
    #     if pay_account_id is None:
    #         if self.balance - amount >= 0.0:
    #             self.balance -= amount
    #             self.credit_limit = self.DEFAULT_CREDIT_LIMIT
    #         else:
    #             raise ValueError("No pay account and card balance is not enough to repay.")
    #     else:
    #         pay_account = CreditCard.objects.get(account_id=pay_account_id)
    #         if pay_account.balance - amount >= 0.0:
    #             pay_account.balance -= amount
    #             self.credit_limit = self.DEFAULT_CREDIT_LIMIT
    #             pay_account.save()
    #         else:
    #             raise ValueError("Both card and pay account's balance is not enough to repay.")
    #     self.save()

    def frozen_card(self, password):
        """冻结信用卡"""
        if password != self.password:
            raise ValueError("密码不匹配")
        elif self.is_frozen:
            raise ValueError("此卡已冻结")
        else:
            self.is_frozen = True
            self.save()
            return True

    def transfer_in(self, delta):
        # 转入金额
        if self.is_frozen or self.is_lost:
            raise ValueError("信用卡已被冻结或挂失")
        else:
            self.balance -= delta
            self.save()

    def transfer_out(self, delta, password):
        # 转出金额
        if self.is_frozen or self.is_lost:
            raise ValueError("已冻结或挂失")
        elif self.password != password:
            raise ValueError("密码错误")
        elif self.credit_limit - self.balance < delta:
            raise ValueError("余额不足")
        else:
            self.balance += delta
            self.save()


class Transaction(models.Model):
    transfer_record_id = models.AutoField(primary_key=True)
    account_in_id = models.IntegerField()
    account_out_id = models.IntegerField()
    transfer_amount = models.IntegerField()
    transfer_date = models.DateTimeField()

    def __str__(self):
        return self.transfer_record_id


# 申请记录
class CreditCardApplication(models.Model):
    apply_id = models.AutoField(primary_key=True)
    online_user = models.ForeignKey(Online_user, on_delete=models.CASCADE)
    creditCardExaminer = models.ForeignKey(CreditCardExaminer, on_delete=models.CASCADE, null=True, default=None)
    apply_status = models.BooleanField(default=False)
    apply_result = models.BooleanField(default=False)
    apply_date = models.DateTimeField(default=timezone.now)

    DEFAULT_CREDIT_LIMIT = 1000.0  # 默认信用额度

    @staticmethod
    def new_apply(online_user_id):
        new_application = CreditCardApplication()
        new_application.online_user = Online_user.objects.get(person_id=online_user_id)
        new_application.save()
        return new_application

    def change_state(self, apply_result, credit_examiner_id):
        self.apply_status = True
        self.apply_result = apply_result
        self.credit_examiner_id = credit_examiner_id
        self.save()

    def get_state(self):
        try:
            application = CreditCardApplication.objects.get(apply_id=self.apply_id)
            if application.apply_status:
                return application.apply_result
            else:
                return "Not ready yet."
        except CreditCardApplication.DoesNotExist:
            raise ValueError("Application not found.")
