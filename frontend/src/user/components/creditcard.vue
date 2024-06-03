<template>
    <el-scrollbar height="100%" style="width: 100%; height: 100%">

      <!--信用卡信息显示卡片-->
      <div style="margin-left:20px; display: flex;flex-wrap: wrap; justify-content: start;">
        <div class="creditcardBox" v-for="creditcard in creditcards" :key="creditcard.account_id">
          <div>
            <!-- 卡片标题 -->
            <div style="font-size: 25px; font-weight: bold;">No. {{creditcard.account_id}}</div>
  
            <el-divider />
  
            <!-- 卡片内容 -->
            <div style="margin-left: 10px; text-align: start; font-size: 16px;">
              <p style="padding: 2.5px;"><span style="font-weight: bold">未还金额：</span>{{creditcard.balance}}</p>
              <p style="padding: 2.5px;"><span style="font-weight: bold">信用额度：</span>{{creditcard.limit}}</p>
              <p style="padding: 2.5px;"><span style="font-weight: bold">开户日期：</span>{{creditcard.due_date}}</p>
              <p style="padding: 2.5px;">
                <el-tag v-if="creditcard.is_frozen">已冻结</el-tag>
                <el-tag v-if="creditcard.is_lost" style="margin-left: 10px">已挂失</el-tag>
                <el-tag v-if="!creditcard.is_frozen && !creditcard.is_lost">正常</el-tag>
              </p>
            </div>
            <el-divider />

            <!-- 卡片操作 -->
            <div style="margin-top: 10px; display:flex">
              <el-button @click="this.newFreezeCredit.account_id=creditcard.account_id,
                this.freezeCreditVisible=true" style="background-color: #87CEEB;">冻结</el-button>
              <el-button  @click="this.newReportLoss.account_id=creditcard.account_id,
                this.ReportLoss = true" style="background-color: #87CEEB;" >挂失</el-button>
              <el-button  @click="this.newUpdateLimit.account_id=creditcard.account_id,
                this.UpdateLimit=true" style="background-color: #87CEEB; width: 95px;">
                更新额度
              </el-button>
            </div>

            <div style="margin-top: 3px; display:flex" >
              <el-button  @click="this.newPayBill.account_id=creditcard.account_id,
                this.PayBill=true" style="background-color: #87CEEB;">
                付款
              </el-button>
              <el-button @click="this.newRepayCredit.account_id=creditcard.account_id,
                this.RepayCredit=true" style="background-color: #87CEEB;">
                还款
              </el-button>
              <el-button  @click="this.billInfo.account_id=creditcard.account_id,
              this.ViewBill = true" style="background-color: #87CEEB;">查看月账单</el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 冻结对话框 -->
      <el-dialog v-model="freezeCreditVisible" title="冻结信用卡" width="30%" align-center>
      <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          密码：
          <el-input v-model="newFreezeCredit.password" style="width: 12.5vw;" clearable />
      </div>
      <template #footer>
          <span>
              <el-button @click="this.freezeCreditVisible = false">取消</el-button>
              <el-button type="primary" @click="ConfirmFreezeCredit"
                  :disabled="newFreezeCredit.password.length === 0">确定</el-button>
          </span>
      </template>
      </el-dialog>

      <!-- 挂失对话框 -->
      <el-dialog v-model="ReportLoss" title="挂失信用卡" width="30%" align-center>
        <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
            密码：
            <el-input v-model="newReportLoss.password" style="width: 12.5vw;" clearable />
        </div>

        <template #footer>
            <span>
                <el-button @click="this.ReportLoss = false">取消</el-button>
                <el-button type="primary" @click="ConfirmReportLoss"
                    :disabled="newReportLoss.password.length === 0">确定</el-button>
            </span>
        </template>
        </el-dialog>

      <!--更新额度对话框-->
      <el-dialog v-model="UpdateLimit" title="更新额度" width="30%" align-center>
        <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          输入密码：
          <el-input v-model="newUpdateLimit.password" style="width: 12.5vw;" clearable />
        </div>
        <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
          更新额度：
          <el-input v-model="newUpdateLimit.limit" style="width: 12.5vw;" clearable />
        </div>

        <template #footer>
                <span>
                    <el-button @click="this.UpdateLimit = false">取消</el-button>
                    <el-button type="primary" @click="ConfirmUpdateLimit"
                        :disabled="newUpdateLimit.account_id.length === 0 || newUpdateLimit.limit.length === 0">确定</el-button>
                </span>
            </template>
      </el-dialog>

      <!--付款对话框-->
      <el-dialog v-model="PayBill" title="付款服务" width="30%" align-center>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                收款账号：
                <el-input v-model="newPayBill.PayTo_id" style="width: 12.5vw;" clearable />
            </div>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                支付金额：
                <el-input v-model="newPayBill.amount" style="width: 12.5vw;" clearable />
            </div>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                输入密码：
                <el-input v-model="newPayBill.password" style="width: 12.5vw;" clearable />
            </div>
            
            <template #footer>
                <span>
                    <el-button @click="this.PayBill = false">取消</el-button>
                    <el-button type="primary" @click="ConfirmPayBill"
                        :disabled="newPayBill.PayTo_id.length === 0
                        || newPayBill.amount.length === 0
                        || newPayBill.password.length === 0">确定</el-button>
                </span>
            </template>
        </el-dialog>

      <!--还款对话框-->
      <el-dialog v-model="RepayCredit" title="还款服务" width="30%" align-center>
          <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
              支付卡号：
              <el-input v-model="newRepayCredit.pay_account" style="width: 12.5vw;" clearable />
          </div>
          <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
              支付密码：
              <el-input v-model="newRepayCredit.pay_password" style="width: 12.5vw;" clearable />
          </div>
          <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
              还款金额：
              <el-input v-model="newRepayCredit.amount" style="width: 12.5vw;" clearable />
          </div>

          <template #footer>
              <span>
                  <el-button @click="this.RepayCredit = false">取消</el-button>
                  <el-button type="primary" @click="ConfirmRepayCredit"
                      :disabled="newRepayCredit.amount.length === 0 || newRepayCredit.pay_password.length === 0
                      || newRepayCredit.pay_account.length === 0">确定</el-button>
              </span>
          </template>
      </el-dialog>

      <!--查看月账单-->
      <el-dialog v-model="ViewBill" title="查看月账单" width="50%" align-center>
        <div style="display: flex;">
          <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px;">
            年份：
            <el-input v-model="billInfo.year" style="width: 8vw;" clearable />
          </div>
          <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px;">
            月份：
            <el-input v-model="billInfo.month" style="width: 6vw;" clearable />
          </div>
          <div style="margin-left: 2vw; margin-top: 20px; text-align: center;">
            <el-button type="primary" @click="ConfirmQueryBill">查询</el-button>
          </div>
          <div style="margin-left: 2vw; margin-top: 20px; text-align: center;">
          <el-button type="primary" @click="isShow=false,ViewBill=false">退出</el-button>
        </div>
        </div>

        <el-table v-if="isShow" :data="bills" :table-layout="'auto'"
          :default-sort="{ prop: 'date', order: 'ascending' }"
          style="width: 100%; margin-left: 10px; margin-top: 30px; margin-right: 50px; max-width: 80vw;">
          <el-table-column prop="bill_record_id" label="账单号" sortable />
          <el-table-column prop="account_in_id" label="付款账号" sortable />
          <el-table-column prop="account_out_id" label="收款账号" />
          <el-table-column prop="date" label="交易时间" />
          <el-table-column prop="amount" label="交易金额" />
        </el-table>
      </el-dialog>

    </el-scrollbar>
  </template>

<script>
import axios from "axios";
import {ElMessage} from "element-plus";

export default{
  data(){
    return{
      online_user_id: 1,
      creditcards: [
        {
          account_id: 1,
          due_date: '2025-10-1',
          limit: 1000,
          balance: 106.3,
          is_frozen: false,
          is_lost: false,
          online_user_id: '10000', // online_user_id
          card_type: '信用卡', // credit card
        },
      ],
      // frozen
      freezeCreditVisible: false,
      newFreezeCredit: {
        account_id: '',
        password: '',
      },
      // report loss
      ReportLoss: false,
      newReportLoss: {
        account_id: '',
        password: '',
      },
      // update limits
      UpdateLimit: false,
      newUpdateLimit: {
        account_id: '',
        password: '',
        limit: 1500,
      },
      // pay bill
      PayBill: false,
      newPayBill: {
        PayTo_id: 1,
        account_id: 2,
        amount: 1,
        password: '',
      },
      // repay from other card
      RepayCredit: false,
      newRepayCredit: {
        account_id: 1,
        pay_account: 1,
        pay_password: '',
        amount: 1,
      },
      // show month bill
      ViewBill: false,
      isShow: false, // 是否展示结果表格
      total_amount: 0,
      billInfo: {
        account_id: 2,
        year: 2024,
        month: 5,
      },
      bills: [
        {
          bill_record_id: 1,
          account_in_id: 1,
          account_out_id: 2,
          amount: 123,
          date: '2024 5.8-12:00',
        },
      ],

    }
  },
  methods: {
    QueryCards() {
      axios.get("/api/get_cards", {
        params: {
          online_user_id: this.online_user_id
        }
      })
          .then(response => {
            this.creditcards = [];
            let tableData = response.data.list;
            tableData.forEach(item => {
              let card = {
                account_id: item.pk,
                online_user_id: item.fields.online_user,
                balance: item.fields.balance,
                card_type: item.fields.card_type,
                due_date: item.fields.due_date,
                limit: item.fields.credit_limit,
                is_frozen: item.fields.is_frozen,
                is_lost: item.fields.is_lost,
              };
              this.creditcards.push(card);
            });
          })
          .catch(error => {
                console.error('Error fetching examiners:', error);
                ElMessage.error("数据获取失败，请稍后重试！" + error);
              });
    },
    ConfirmFreezeCredit() {
      console.log("freeze:" + this.newFreezeCredit.account_id)
      axios.post("/api/frozen_card",
      {
        account_id: this.newFreezeCredit.account_id,
        password: this.newFreezeCredit.password,
      })
          .then(response => {
            if (response.data.status === 'success') {
              ElMessage.success("冻结成功");
              this.freezeCreditVisible = false;
              this.QueryCards();
            } else {
              ElMessage.error("冻结失败: " + response.data.message);
            }
          })
          .catch(error => {
            console.error('Error ConfirmChangeState:', error);
            ElMessage.error("冻结失败" + error);
          });
    },
    ConfirmReportLoss() {
      axios.post("/api/lost_card",
      {
        account_id: this.newReportLoss.account_id,
        password: this.newReportLoss.password,
      })
          .then(response => {
            if (response.data.status === 'success') {
              ElMessage.success("冻结成功");
              this.ReportLoss = false;
              this.QueryCards();
            } else {
              ElMessage.error("冻结失败: " + response.data.message);
            }
          })
          .catch(error => {
            console.error('Error ConfirmChangeState:', error);
            ElMessage.error("挂失失败" + error);
          });
    },
    ConfirmUpdateLimit() {
      // console.log("account_id:" + this.newUpdateLimit.account_id)
      axios.post("/api/update_limit",
      {
        account_id: this.newUpdateLimit.account_id,
        password: this.newUpdateLimit.password,
        amount: this.newUpdateLimit.limit,
      })
          .then(response => {
            if (response.data.status === 'success') {
              ElMessage.success("更新成功");
              this.UpdateLimit = false;
              this.QueryCards();
            } else {
              ElMessage.error("更新失败: " + response.data.message);
            }
          })
          .catch(error => {
            console.error('Error ConfirmChangeState:', error);
            ElMessage.error("更新失败" + error);
          });
    },
    ConfirmPayBill() {
      axios.post("/api/pay_to",
      {
        account_out_id: this.newPayBill.account_id,
        account_in_id: this.newPayBill.PayTo_id,
        password: this.newPayBill.password,
        amount: this.newPayBill.amount,
      })
          .then(response => {
            if (response.data.status === 'success') {
              ElMessage.success("支付成功");
              this.PayBill = false;
              this.QueryCards();
            } else {
              ElMessage.error("支付失败: " + response.data.message);
            }
          })
          .catch(error => {
            console.error('Error ConfirmChangeState:', error);
            ElMessage.error("更新失败" + error);
          });
    },
    ConfirmRepayCredit() {
      axios.post("/api/repay",
      {
        account_id: this.newRepayCredit.account_id,
        pay_account: this.newRepayCredit.pay_account,
        pay_password: this.newRepayCredit.pay_password,
        amount: this.newRepayCredit.amount,
      })
          .then(response => {
            if (response.data.status === 'success') {
              ElMessage.success("还款成功");
              this.RepayCredit = false;
              this.QueryCards();
            } else {
              ElMessage.error("还款失败: " + response.data.message);
            }
          })
          .catch(error => {
            console.error('Error ConfirmChangeState:', error);
            ElMessage.error("还款失败" + error);
          });
    },
    ConfirmQueryBill() {
      axios.get("/api/show_month_bill", {
        params: {
          month: this.billInfo.month,
          year: this.billInfo.year,
          account_id: this.billInfo.account_id,
        }
      })
          .then(response => {
            this.bills = [];
            this.total_amount = response.data.total_amount;
            let tableData = response.data.list;
            tableData.forEach(item => {
              let bill = {
                bill_record_id: item.pk,
                account_in_id: item.fields.account_in_id,
                account_out_id: item.fields.account_out_id,
                amount: item.fields.amount,
                date: item.fields.date,
              };
              this.bills.push(bill);
            });
            if (response.data.status === 'success') {
              ElMessage.success("查询成功");
              this.isShow = true;
              this.QueryCards();
            } else {
              ElMessage.error("查询失败: " + response.data.message);
            }
          })
          .catch(error => {
            ElMessage.error("查询失败" + error);
          });
    },
  },
  mounted() {
    this.QueryCards();
  }
}
</script>

<style scoped>
.creditcardBox {
  height:420px;
  width: 275px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  text-align: center;
  margin-top: 40px;
  margin-left: 27.5px;
  margin-right: 10px;
  padding: 7.5px;
  padding-right: 10px;
  padding-top: 15px;
}
.newCreditcardBox {
  height: 420px;
  width: 275px;
  margin-top: 40px;
  margin-left: 27.5px;
  margin-right: 10px;
  padding: 7.5px;
  padding-right: 10px;
  padding-top: 15px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  text-align: center;
}
</style>