import en from './lang/en.json';
import de from './lang/de.json';
import VueI18n from "vue-i18n";
import Vue from "vue";

Vue.use(VueI18n);

export default new VueI18n({
    locale: localStorage.getItem('lang') || 'de',
    messages : {
        en: en,
        de: de
    }
});
