require('./bootstrap');

window.Vue = require('vue');
import Vuetify from 'vuetify';
import { VApp } from "vuetify/lib";
import '@mdi/font/css/materialdesignicons.css'
import i18n from "./i18n";

Vue.component('posts-table', require('./components/PostsTableComponent.vue').default);
Vue.component('profiles-table', require('./components/ProfilesTableComponent').default);
Vue.component('users-table', require('./components/UsersTableComponent').default);
Vue.component('settings-table', require('./components/SettingsTableComponent').default);
Vue.component('categories-table', require('./components/CategoriesTableComponent').default);
Vue.component('lang-changer', require('./components/LangChangerComponent').default);

Vue.use(Vuetify);
Vue.prototype.$userId = document.querySelector("meta[name='user-id']").getAttribute('content');
new Vue({
    i18n,
    vuetify : new Vuetify(),
    iconfont: 'mdi',
    components: {
        VApp
    },
}).$mount('#app');

