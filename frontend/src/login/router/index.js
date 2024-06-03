import { createRouter, createWebHistory} from 'vue-router'
import Manager from "@/login/components/managerLog.vue";
import Cashier from "@/login/components/cashierLog.vue";
import Examiner from "@/login/components/examinerLog.vue";
import User from "@/login/components/userLog.vue";
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/login'
        },
        {
            path: '/login/managerLog',
            component: Manager,
        },
        {
            path: '/login/cashierLog',
            component: Cashier,
        },
        {
            path: '/login/examinerLog',
            component: Examiner,
        },
        {
            path: '/login/userLog',
            component: User,
        },
    ]
})
export default router