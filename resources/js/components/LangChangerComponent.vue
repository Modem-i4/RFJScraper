<template>
    <a class="nav-link" @click="change">{{this.lang === 'en' ? 'DE' : 'EN'}}</a>
</template>
<script>
    export default {
        name: "LangChanger",
        data() {
            return {
                lang: localStorage.getItem('lang') || 'de'
            }
        },
        methods: {
            change() {
                let newLang = this.lang === 'en' ? 'de' : 'en'
                localStorage.setItem('lang', newLang);
                window.location.replace('/set_locale/'+newLang)
            }
        }
    }
</script>
<style>
    a {
        cursor: pointer;
    }
</style>
