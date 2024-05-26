import { createRouter, createWebHistory} from 'vue-router'
import Home from "@/manager/components/home.vue";
import Credit_card_examiner from "@/manager/components/credit_card_examiner.vue";
//import 自定义组件名 from 路径
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [

        {
            path: '/',
            redirect: '/manager/home'
        },
        {
            path: '/manager/home',
            component: Home,
        },
        {
            path: '/manager/credit_card_examiner',
            component: Credit_card_examiner,
        },
    ]
})

export default router