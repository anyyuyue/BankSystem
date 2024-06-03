<template>
    <el-scrollbar height="100%" style="width: 100%; height: 100%">

      <!--信用卡信息显示卡片-->
      <div style="margin-left:20px; display: flex;flex-wrap: wrap; justify-content: start;">
        <div class="creditcardBox" v-for="creditcard in creditcards" :key="creditcard.id">
          <div>
            <!-- 卡片标题 -->
            <div style="font-size: 25px; font-weight: bold;">No. {{creditcard.id}}</div>
  
            <el-divider />
  
            <!-- 卡片内容 -->
            <div style="margin-left: 10px; text-align: start; font-size: 16px;">
              <p style="padding: 2.5px;"><span style="font-weight: bold">卡号：</span>{{creditcard.account_id}}</p>
              <p style="padding: 2.5px;"><span style="font-weight: bold">余额：</span>{{creditcard.balance}}</p>
              <p style="padding: 2.5px;"><span style="font-weight: bold">种类：</span>{{creditcard.card_type}}</p>
              <p style="padding: 2.5px;"><span style="font-weight: bold">有效期：</span>{{creditcard.due_date}}</p>
              <p style="padding: 2.5px;"><span style="font-weight: bold">借款上限：</span>{{creditcard.limit}}</p>
              <p style="padding: 2.5px;">
                <el-tag v-if="creditcard.is_frozen">已冻结</el-tag>
                <el-tag v-if="creditcard.is_lost" style="margin-left: 10px">已挂失</el-tag>
                <el-tag v-if="!creditcard.is_frozen && !creditcard.is_lost">正常</el-tag>
              </p>
            </div>
            <el-divider />

            <!-- 卡片操作 -->
            <div style="margin-top: 10px; display:flex">
              <el-button type="freeze" @click="this.FreezeCredit = true" style="background-color: #87CEEB;">
                冻结
              </el-button>
              <el-button type="report_loss" @click="this.ReportLoss = true" style="background-color: #87CEEB;" >
                挂失
              </el-button>
              <el-button type="view_month_bill" @click="this.ViewBill = true" style="background-color: #87CEEB;">
                查看月账单
              </el-button>
            </div>

            <div style="margin-top: 3px; display:flex" >
              <el-button type="repay_credit" @click="this.RepayCredit = true" style="background-color: #87CEEB;">
                还款
              </el-button>
              <el-button type="pay_bill" @click="this.PayBill = true" style="background-color: #87CEEB;">
                付款
              </el-button>
              <el-button type="pay_bill" @click="this.UpdateLimit = true" style="background-color: #87CEEB; width: 95px;">
                更新额度
              </el-button>
            </div>
          </div>
        </div>

        <el-button class="newCreditcardBox" @click="newCardVisible = true">
          <el-icon style="height: 50px; width: 50px;">
            <Plus style="height: 100%; width: 100%;" />
          </el-icon>
        </el-button>
      </div>

        <!--冻结-->
        <el-dialog v-model="FreezeCredit" title="冻结信用卡" width="30%" align-center>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                信用卡ID：
                <el-input v-model="newFreezeCredit.account_id" style="width: 12.5vw;" clearable />
            </div>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                密码：
                <el-input v-model="newFreezeCredit.password" style="width: 12.5vw;" clearable />
            </div>
            <template #footer>
                <span>
                    <el-button @click="this.FreezeCredit = false">取消</el-button>
                    <el-button type="primary" @click="ConfirmFreezeCredit"
                        :disabled="newFreezeCredit.password.length === 0">确定</el-button>
                </span>
            </template>
        </el-dialog>

      <!--挂失-->
      <el-dialog v-model="ReportLoss" title="挂失信用卡" width="30%" align-center>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                信用卡ID：
                <el-input v-model="newReportLoss.account_id" style="width: 12.5vw;" clearable />
            </div>
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

      <!--付款-->
      <el-dialog v-model="PayBill" title="付款服务" width="30%" align-center>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                商家ID：
                <el-input v-model="newPayBill.PayTo_id" style="width: 12.5vw;" clearable />
            </div>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                信用卡ID：
                <el-input v-model="newPayBill.account_id" style="width: 12.5vw;" clearable />
            </div>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                金额：
                <el-input v-model="newPayBill.amount" style="width: 12.5vw;" clearable />
            </div>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                密码：
                <el-input v-model="newPayBill.password" style="width: 12.5vw;" clearable />
            </div>
            
            <template #footer>
                <span>
                    <el-button @click="this.PayBill = false">取消</el-button>
                    <el-button type="primary" @click="ConfirmPayBill"
                        :disabled="newPayBill.PayTo_id.length === 0 || newPayBill.account_id.length === 0 || newPayBill.password.length === 0">确定</el-button>
                </span>
            </template>
        </el-dialog>


        <!--还款-->
        <el-dialog v-model="RepayCredit" title="还款服务" width="30%" align-center>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                信用卡ID：
                <el-input v-model="newRepayCredit.account_id" style="width: 12.5vw;" clearable />
            </div>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                还款金额：
                <el-input v-model="newRepayCredit.amount" style="width: 12.5vw;" clearable />
            </div>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                密码：
                <el-input v-model="newRepayCredit.password" style="width: 12.5vw;" clearable />
            </div>
            
            <template #footer>
                <span>
                    <el-button @click="this.RepayCredit = false">取消</el-button>
                    <el-button type="primary" @click="ConfirmRepayCredit"
                        :disabled="newRepayCredit.amount <= 0 || newRepayCredit.password.length === 0">确定</el-button>
                </span>
            </template>
        </el-dialog>
        
        <!--查看月账单-->
        <el-dialog v-model="ViewBill" title="查看月账单" width="50%" align-center>
            <el-table :data="fitlerBills" height="600"
            :default-sort="{ prop: 'bill_record_id', order: 'ascending' }" :table-layout="'auto'"
            style="width: 100%; margin-left: 10px; margin-top: 30px; margin-right: 50px; max-width: 80vw;">

            <el-table-column prop="bill_record_id" label="账单记录ID" sortable/>
            <el-table-column prop="account_id" label="账户ID" sortable/>
            <el-table-column prop="payTo_id" label="商家ID" />
            <el-table-column prop="amount" label="消费金额" />
            </el-table>
        </el-dialog>

      <!--更新额度-->
      <el-dialog v-model="UpdateLimit" title="更新额度" width="30%" align-center>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                信用卡ID：
                <el-input v-model="newUpdateLimit.account_id" style="width: 12.5vw;" clearable />
            </div>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                申请额度：
                <el-input v-model="newUpdateLimit.newlimit" style="width: 12.5vw;" clearable />
            </div>

            <template #footer>
                <span>
                    <el-button @click="this.UpdateLimit = false">取消</el-button>
                    <el-button type="primary" @click="ConfirmUpdateLimit"
                        :disabled="newUpdateLimit.account_id.length === 0 || newUpdateLimit.newlimit.length === 0">确定</el-button>
                </span>
            </template>
        </el-dialog>

    </el-scrollbar>
  </template>

<script>
  export default{
    computed: {
        fitlerBills() {
            return this.bills
        }
    },
    data(){
      return{
        FreezeCredit: false,
        ReportLoss: false,
        ViewBill: false,
        RepayCredit: false,
        PayBill: false,
        UpdateLimit: false,

        newFreezeCredit: {
          account_id: '',
          password: '',
        },
        newReportLoss: {
          account_id: '',
          password: '',
        },
        newPayBill: {
          PayTo_id: '',
          account_id: '',
          amount: '',
          password: '',
        },
        newRepayCredit: {
          account_id: '',
          amount: '',
          password: '',
        },
        newUpdateLimit: {
          account_id: '',
          password: '',
        },

        bills: [
          {
            bill_record_id: '12',
            account_id: '123',
            card_id: '400321',
            payTo_id: '111',
            amount: 123,
          },
          {
            bill_record_id: '2',
            account_id: '234',
            card_id: '400322',
            payTo_id: '1234',
            amount: 23,
          },
        ],

        creditcards: [
          {
            id: 1,
            account_id: '10000',
            balance: 106.3,
            card_type: 'user',
            due_date: '2025-10-1',
            limit: 1000,
            is_frozen: false,
            is_lost: false,
          },
          {
            id: 2,
            account_id: '10001',
            balance: 10.2,
            card_type: 'user',
            due_date: '2045-4-1',
            limit: 1000,
            is_frozen: true,
            is_lost: true,
          },
          {
            id:3,
            account_id: '10003',
            balance: 11.0,
            card_type: 'user',
            due_date: '2025-3-1',
            limit: 1000,
            is_frozen: true,
            is_lost: false,
          },
          {
            id:4,
            account_id: '10004',
            balance: 11.0,
            card_type: 'user',
            due_date: '2025-3-1',
            limit: 1000,
            is_frozen: true,
            is_lost: false,
          },
        ],
      }
    },
    methods: {
      ShowCards() {
        axios.get("/api/show_cards")
          .then(response => {
            this.card
          })
      }
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