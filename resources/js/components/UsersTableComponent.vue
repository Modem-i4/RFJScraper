<template>
    <v-app>
        <v-card-title>
            <h2>{{$t('Users')}}</h2>
            <v-spacer></v-spacer>
            <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                :label="$t('Search')"
                single-line
                hide-details
                autocomplete="nope"
                clearable
            />
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
            <template #item.role="{ item }">
                <v-select
                    :items="roles"
                    v-model="item.role"
                    label="Role"
                    :disabled="item.id <= user_id"
                    required
                    @change="changeRole(item.id, item.role)"
                />
            </template>
            <template #item.notifications_receiver="{ item }">
                <v-checkbox v-model="item.notifications_receiver"
                            @change="changeNotificationReceiver(item.id, item.notifications_receiver)"/>
            </template>
        </v-data-table>
    </v-app>
</template>

<script>
    import DataTableCore from "../mixins/DataTableCore";

    export default {
        mixins: [DataTableCore],
        data () {
            return {
                crudApiEndpoint: '/api/users',
                roles: ['user', 'redactor', 'manager', 'admin'],
                headers: [
                    {text: this.$t('id'), value: 'id', width: '2%'},
                    {text: this.$t('Name'), value: 'name'},
                    {text: this.$t('E-mail'), value: 'email'},
                    {text: this.$t('Role'), value: 'role'},
                    {text: this.$t('Registration'), value: 'reg_time'},
                    {text: this.$t('News Notifications'), value: 'notifications_receiver'},
                ],
            }
        },
        methods: {
            changeRole($id, $newRole) {
                axios.post(this.crudApiEndpoint + "/role/" + $id + "/" + $newRole)
            },
            changeNotificationReceiver($id, $newState) {
                axios.post(this.crudApiEndpoint + "/news/" + $id + "/" + $newState)
            },
        },
        props: {
            user_id: {
                default: -1
            }
        }
    }
</script>
