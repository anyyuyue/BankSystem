<template>
    <el-scrollbar height="100%" style="width: 100%;">

    <!-- 标题 -->
    <div style="margin-top: 20px; margin-left: 40px; font-size: 2em; font-weight: bold;">
        已审核
    </div>

    <!-- 记录 --> 
    <el-table :data="tableData" height="600"
        :default-sort="{ prop: 'apply_id', order: 'ascending' }" :table-layout="'auto'"
        style="width: 100%; margin-left: 50px; margin-top: 30px; margin-right: 50px; max-width: 80vw;">

        <el-table-column prop="apply_id" label="申请序号" sortable/>
        <el-table-column prop="apply_date" label="申请时间" sortable/>
        <el-table-column prop="account_id" label="申请人ID" />
        <el-table-column prop="asset" label="申请人信誉" />
        <el-table-column prop="examiner_id" label="审核员ID" /> 
        <el-table-column prop="apply_result" label="申请结果" />
        <el-table-column label="具体操作">
          <template v-slot="scope">
            <el-button link type="primary" size="small" @click="this.newCardVisible=true,
              this.newCardUserId=scope.row.account_id">开户</el-button>
          </template>

        </el-table-column>
    </el-table>

    <!-- 开户对话框 -->
    <el-dialog v-model="newCardVisible" title="开户" width="30%" align-center>
      确认要开户吗？
      <template #footer>
        <span>
          <el-button @click="this.newCardVisible = false">取消</el-button>
          <el-button type="primary" @click="ConfirmNewCard">确认</el-button>
        </span>
      </template>
    </el-dialog>

    </el-scrollbar>
</template>

<script>

import axios from "axios";
import {ElMessage} from "element-plus";

export default {
  data() {
    return {
      tableData: [
        {
          apply_id:1,
          apply_date: "2024-03-04 21:49:00",
          apply_result: true,
          account_id: 1, // online_user_id
          asset: 'good',
          examiner_id: 1,
        },
      ],
      // 开户
      newCardVisible: false,
      newCardUserId: 1,
    }
  },
  methods: {
    QueryApplications() {
      axios.get("/api/get_check_applications")
          .then(response => {
            this.tableData = [];
            let tableData = response.data.list;
            tableData.forEach(item => {
              let application = {
                apply_id: item.pk,
                apply_date: item.fields.apply_date,
                apply_result: item.fields.apply_result,
                account_id: item.fields.online_user,
                assert: "unset", // 这里假设没有从后端获取 assert
                examiner_id: item.fields.creditCardExaminer,
              };
              this.tableData.push(application);
            });
          })
    },
    ConfirmNewCard() {
      axios.post("/api/add_new_card",
      {
        online_user_id: this.newCardUserId,
      })
          .then(response => {
              ElMessage.success("修改成功")
              this.newCardVisible = false
              this.QueryApplications()
          })
          .catch(error => {
            console.error('Error fetching examiners:', error);
            ElMessage.error("修改失败" + error);
          });
    },
  },
  mounted() {
    this.QueryApplications()
  }
}
</script>

<style scoped>
</style>