<template>
    <v-app>
        <v-card-title>
            <h2>{{ $t('Settings') }}</h2>
        </v-card-title>
        <v-data-table
            :footer-props="footerOptions"
            :headers="headers"
            :items="items"
            :options.sync="options"
            :server-items-length="pagination.total"
            :loading="loading"
            :search="search"
            class="elevation-1"
        >
            <template #item.alias="{ value }">
                {{$t(value)}}
            </template>
            <template #item.value="{ item }">
                <vue-numeric-input v-model="item.value" @input="item.enabled=true" :min="item.min_value" :max="item.max_value"/>
            </template>
            <template #item.default_value="{ item }">
                {{item.default_value}}
                <v-icon small
                    @click="item.value = item.default_value; item.enabled=true"
                >mdi-restore</v-icon>
            </template>
            <template #item.save="{ item }">
                <v-icon @click="save(item.id, item.value)" :disabled="!item.enabled">mdi-content-save</v-icon>
            </template>
        </v-data-table>
    </v-app>
</template>

<script>
    import DataTableCore from "../mixins/DataTableCore";
    import VueNumericInput from 'vue-numeric-input'

    export default {
        mixins: [DataTableCore],
        components: {
            VueNumericInput
        },
        data () {
            return {
                crudApiEndpoint: '/api/settings',
                headers: [
                    {text: this.$t('Setting'), value: 'alias'},
                    {text: this.$t('Value (minutes)'), value: 'value'},
                    {text: this.$t('Default value'), value: 'default_value'},
                    {text: this.$t('Save'), value: 'save'},
                ],
            }
        },
        methods: {
            save($id, $newValue) {
                this.loading = true
                axios.post(this.crudApiEndpoint + "/value/" + $id + "/" + $newValue)
                .then(this.fetch)
            },
        }
    }
</script>
