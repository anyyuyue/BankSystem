<template>
    <el-scrollbar height="100%" style="width: 100%;">

    <!-- 标题 -->
    <div style="margin-top: 20px; margin-left: 40px; font-size: 2em; font-weight: bold;">
        已审核
    </div>

    <!-- 记录 --> 
    <el-table :data="fitlerTableData" height="600"
        :default-sort="{ prop: 'apply_id', order: 'ascending' }" :table-layout="'auto'"
        style="width: 100%; margin-left: 50px; margin-top: 30px; margin-right: 50px; max-width: 80vw;">

        <el-table-column prop="apply_id" label="申请序号" sortable/>
        <el-table-column prop="account_id" label="申请人ID" />
        <el-table-column prop="asset" label="申请人信誉" />
        <el-table-column prop="examiner_id" label="审核员ID" /> 
        <el-table-column prop="result" label="申请结果" />
    </el-table>

    </el-scrollbar>
</template>

<script>

export default {
    data() {
        return {
            tableData: [
                { 
                    apply_id:'1',
                    account_id: '123',
                    asset: 'good',
                    examiner_id: '111',
                    result: '通过',
                },
                {
                    apply_id: '2',
                    account_id: '1234',
                    asset: 'good',
                    examiner_id: '123',
                    result: '通过',
                },
                {
                    apply_id: '3',
                    account_id: '123',
                    asset: 'middling',
                    examiner_id: '12',
                    result: '不通过',
                }
            ]
        }
    },
    computed: {
        fitlerTableData() {
            return this.tableData
        }
    },
}
</script>

<style scoped>
</style>