<template>
    <el-scrollbar height="100%" style="width: 100%;">

    <!-- 标题 -->
    <div style="margin-top: 20px; margin-left: 40px; font-size: 2em; font-weight: bold;">
        未审核
    </div>

    <!-- 记录 -->
    <el-table :data="fitlerTableData" height="600"
        :default-sort="{ prop: 'apply_id', order: 'ascending' }" :table-layout="'auto'"
        style="width: 100%; margin-left: 50px; margin-top: 30px; margin-right: 50px; max-width: 80vw;">
        <el-table-column prop="apply_id" label="申请序号" sortable/>
        <el-table-column prop="account_id" label="申请人ID" />
        <el-table-column prop="asset" label="申请人信誉" />

        <el-table-column label="操作">
            <!--<template #default="scope">-->
                <el-button link type="primary" size="small" @click="this.checkAsset = true">审核</el-button><!--disabled="scope.row.asset !== 'good' && scope.row.asset!='very good'"-->
            <!--</template>-->
        </el-table-column>
    </el-table> 

        <!--审核-->
        <el-dialog v-model="checkAsset" title="审核" width="30%" align-center>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                审核员ID：
                <el-input v-model="ApplyResult.examiner_id" style="width: 12.5vw;" clearable />
            </div>
            <div style="margin-left: 2vw; font-weight: bold; font-size: 1rem; margin-top: 20px; ">
                信誉：
                <el-input v-model="ApplyResult.asset" style="width: 12.5vw;" clearable />
            </div>
            
            <template #footer>
                <span>
                    <el-button @click="this.checkAsset = false">取消</el-button>
                    <el-button type="primary" @click="NotPass"
                        :disabled="ApplyResult.examiner_id.length === 0 || ApplyResult.asset==='good' || ApplyResult.asset==='very good'">不通过</el-button>
                    <el-button type="primary" @click="Pass"
                        :disabled="ApplyResult.examiner_id.length === 0 || (ApplyResult.asset!='good' && ApplyResult.asset!='very good')">通过</el-button>
                </span>
            </template>
        </el-dialog>

    </el-scrollbar>
</template>

<script>
export default {
    data() {
        return {
            checkAsset : false,
            ApplyResult: {
                examiner_id: '',
                asset: '',
            },
            tableData: [
                {
                    apply_id:'123',
                    account_id: '123',
                    asset: 'good',
                },
                {
                    apply_id: '122',
                    account_id: '1234',
                    asset: 'middling',
                },
                {
                    apply_id: '111',
                    account_id: '12',
                    asset: 'good',
                }
            ],
        }
    },
    computed: {
        fitlerTableData() { // 搜索规则
            return this.tableData
            //return this.tableData.filter(
            //    (tuple) =>
            //        (this.toSearch == '') || // 搜索框为空，即不搜索
            //        tuple.bookID == this.toSearch || // 图书号与搜索要求一致
            //        tuple.borrowTime.toString().includes(this.toSearch) || // 借出时间包含搜索要求
            //       tuple.returnTime.toString().includes(this.toSearch) // 归还时间包含搜索要求
            //)
        }
    },
}
</script>

<style scoped>
</style>