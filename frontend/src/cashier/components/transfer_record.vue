<!--信用卡模块给柜台提供的查询交易记录的接口-->
<template>
    <el-scrollbar height="100%" style="width: 100%;">

        <!-- 标题 -->
        <div style="margin-top: 20px; margin-left: 40px; font-size: 2em; font-weight: bold;">
            交易记录查询
        </div>

        <!-- 查询框 -->
        <div style="margin-left: 40px;margin-top: 20px">请输入要查询账号的ID、查询的年月进行账单查询 </div>

        <div style="width:60%;display: flex;margin:0 auto; padding-top:5vh;">

          <el-input v-model="this.toQueryInID" style="display:inline; " placeholder="输入交易账号"></el-input>
          <el-input v-model="this.toQueryYear" style="display:inline; " placeholder="输入查询账单年份"></el-input>
          <el-input v-model="this.toQueryMonth" style="display:inline; " placeholder="输入查询账单月份"></el-input>
          <el-button style="margin-left: 10px;" type="primary" @click="QueryMonthBill">查询</el-button>
        </div>

        <!-- 结果表格 -->
        <el-table v-if="isShowTable" :data="tableData"  stripe max-height="600"
                  :default-sort="{ prop: 'transfer_record_id', order: 'ascending' }" :table-layout="'auto'"
                  style="width: 100%; margin-left: 50px; margin-top: 30px; margin-right: 50px; max-width: 80vw;">
          <el-table-column prop="transfer_record_id" label="交易 ID" />
          <el-table-column prop="account_in_id" label="付款人账号" sortable/>
          <el-table-column prop="account_out_id" label="收款人账号" sortable />
          <el-table-column prop="transfer_amount" label="交易金额" sortable />
          <el-table-column prop="transfer_date" label="交易时间" sortable />
        </el-table>

        <div v-if="isShowAmount" style="margin-left: 50px; margin-top: 20px; font-weight:bold">
          本月共支出{{out_amount}}元， 收入{{in_amount}}元， 结余：{{total_amount}}元
        </div>

    </el-scrollbar>
</template>

<script>
import axios from 'axios';
import { Search } from '@element-plus/icons-vue'
import {ElMessage} from "element-plus";

export default {
  data() {
    return {
      isShowTable: false, // 结果表格展示状态
      isShowAmount: false,
      total_amount: 0,
      in_amount:0,
      out_amount:0,
      tableData: [{ // 列表项
        transfer_record_id: 1,
        account_in_id: 1,
        account_out_id: 1,
        transfer_amount: 0,
        transfer_date: ""
      }],
      toQueryInID: '',
      toQueryYear: '',
      toQueryMonth: '',
      toSearch: '',

      Search
    }
  },
  methods: {
    async QueryMonthBill() {
      this.tableData = [] // 清空列表
      try {
        const response = await axios.get('/creditcard/show_month_bill', {
          params: {
            account_id: this.toQueryInID,
            year: this.toQueryYear,
            month: this.toQueryMonth,
          }
        });
        const records = response.data.list; // 获取响应负载
        if(response.data.status === 'success'){
          records.forEach(record => {
            this.tableData.push({
              transfer_record_id: record.transfer_record_id,
              account_in_id: record.account_in_id,
              account_out_id: record.account_out_id,
              transfer_amount: record.transfer_amount,
              transfer_date: record.transfer_date,
            });
          });
          this.total_amount = response.data.total_amount;
          this.in_amount =response.data.in_amount;
          this.out_amount = response.data.out_amount;
          this.isShowTable = true; // 显示结果列表
          this.isShowAmount = true;
          ElMessage.success("查询成功！");
        }else{
          ElMessage.warning(response.data.message);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
        ElMessage.error('数据获取失败，请稍后重试！'+ error);
      }
    }
  },
}
</script>