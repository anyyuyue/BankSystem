import { createRouter, createWebHistory} from 'vue-router'
//import 自定义组件名 from 路径
import Unchecked from '@/examiner/components/unchecked.vue'
import Checked from '@/examiner/components/checked.vue'
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/examiner'
        },
        {
            path: '/examiner/checked',
            component: Checked,
        },
        {
            path: '/examiner/unchecked',
            component: Unchecked,
        },
    ],
})

export default router