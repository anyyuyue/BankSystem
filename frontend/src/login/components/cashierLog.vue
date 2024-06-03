<template>
  <el-scrollbar height="100%" style="width: 100%;">
  <div style="margin-top: 20px; margin-left: 40px; font-size: 2em; font-weight: bold;">
      出纳员登录
  </div>
  <div style="width:30%;margin:0 auto; padding-top:5vh;">
        <div style="height: 20px"></div>
            <div style = "margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
                ID：
                <el-input v-model="Log.id" style="width: 12.5vw; margin-left: 1rem" clearable/>
            </div>
        <div style="height: 20px"></div>
            <div style = "margin-left: 3vw; font-weight: bold; font-size: 1rem; margin-top: 5px;">
                密码：
            <el-input v-model="Log.password" style="width: 12.5vw; margin-left: 1rem" type="password" clearable/>
            </div>
        <div style="height: 20px"></div>
            <div style = "margin-left: 4.3vw; font-weight: bold; font-size: 1rem; margin-top: 5px; ">
            <el-button type="primary" style="margin-left: 57px" @click="submit()">确认登录</el-button>
        </div>
    </div>
  </el-scrollbar>
</template>

<script>
export default {
    data() {
        return {
            Log: {
                id: '',
                password: '',
            }
        }
    },
}
</script>
  
<style scoped>
</style>