
const routes = [
    { path: '/', component: main },
]

const router = new VueRouter({
    routes
})

const app = new Vue({
    router
}).$mount('#app')
