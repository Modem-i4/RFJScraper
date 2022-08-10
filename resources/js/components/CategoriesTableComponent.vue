<template>
    <v-app>
        <v-card-title>
            <h2 class="col-lg-3">{{ $t('Categories') }}</h2>
            <v-card class="px-5 col-lg-6 d-lg-inline-flex">
                <h4 class="my-auto text-nowrap mx-1">{{$t('Add a category')}}</h4>
                <v-form v-model="valid" class="d-lg-inline-flex w-100"
                    @submit.prevent="add">
                    <v-text-field :label="$t('New category name')"
                                  :rules="[rules.minLength, unique, this.serverOk]"
                                  v-model="newCategory"
                                  @input="serverOk = true"
                                  class="col-lg-9"
                                  autocomplete="nope"
                    />
                    <v-btn
                        class="my-auto mx-1 col-lg-3"
                        type="submit"
                        :disabled="!valid || this.newCategory === ``"
                    >Add</v-btn>
                </v-form>
            </v-card>
            <div class="col-lg-3">
                <v-text-field
                    v-model="search"
                    append-icon="mdi-magnify"
                    :label="$t('Search')"
                    single-line
                    hide-details
                    clearable
                ></v-text-field>
            </div>
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
            <template #item.display="{ item }">
                <v-checkbox v-model="item.display" @change="changeDisplay(item.id, item.display)"/>
            </template>

            <template #item.remove="{ item }">
                <v-btn @click="remove(item.id)">
                    <v-icon>mdi-delete</v-icon>
                </v-btn>
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
                crudApiEndpoint: '/api/categories',
                newCategory: '',
                headers: [
                    {text: this.$t('id'), value: 'id'},
                    {text: this.$t('name'), value: 'name'},
                    {text: this.$t('total'), value: 'total'},
                    {text: this.$t('display'), value: 'display', width: "12%"},
                    {value: 'remove', width: "12%"},
                ],
                valid: false,
                serverOk: true,
                rules: {
                    minLength(value) {
                        if (value.length > 3 || value.length === 0) {
                            return true;
                        }
                        return this.$t('Category name is too short')
                    },
                },
            }
        },
        computed: {
            unique() {
                for (let item of this.items) {
                    if(item.name.toLowerCase() === this.newCategory.toLowerCase())
                        return this.$t('This category already exist')
                }
                return true;
            }
        },
        methods: {
            changeDisplay ($id, $displayed) {
                axios.post(this.crudApiEndpoint + "/display/" + $id + "/" + $displayed);
            },
            add() {
                this.loading = true
                axios.post(this.crudApiEndpoint + "/add", {'name' : this.newCategory})
                .then(() => {this.success()})
                .catch(error => this.catchFail(error));
            },
            catchFail(error) {
                this.loading = false
                this.serverOk = error.response.data
            },
            success() {
                this.fetch()
                this.newCategory = ''
                this.valid = true
            },
            remove($id) {
                this.loading = true
                axios.post(this.crudApiEndpoint + '/remove/' + $id)
                .then(x => this.fetch())
            }
        },
    }
</script>

