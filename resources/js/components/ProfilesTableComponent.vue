<template>
    <v-app>
        <v-card-title>
            <h2 class="col-lg-3">{{ $t('Profiles') }}</h2>
            <v-card class="px-5 col-lg-6 d-lg-inline-flex">
                <h4 class="my-auto text-nowrap mx-1">{{ $t('Watch a new profile') }}</h4>
                <v-form v-model="valid" class="d-lg-inline-flex w-100"
                    @submit.prevent="add">
                    <v-text-field :label="$t('New profile URL')"
                                  :error-messages="validate"
                                  v-model="newProfileUrl"
                                  @keydown="requestErrors=''"
                                  autocomplete="nope"
                                  class="col-lg-9"
                    />
                    <v-btn
                        class="my-auto mx-1 col-lg-3"
                        type="submit"
                        :disabled="!valid || this.newProfileUrl === ``"
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
                    autocomplete="nope"
                    clearable
                />
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
            <template #item.picture="{ item }">
                <v-img :src="item.is_group ? `/images/group.jpg` :
                `/images/profiles/${item.id}.jpg`" :alt="item.name" max-width="100px"/>
            </template>
            <template #item.name="{ item }">
                <a :href="item.url" target="_blank">
                    <span>{{item.name }}</span>
                    <v-icon small>mdi-{{indicateSite(item.url)}}</v-icon>
                </a>
            </template>
            <template #item.socNetwork="{ item }">
                {{ item.url !== null ? (item.url.includes('facebook') ? 'facebook' : (item.url.includes('instagram') ? 'instagram' : 'twitter')) : '' }}
            </template>
            <template #item.url="{ item }">
                <v-btn-toggle>
                    <v-btn :href="item.url" target="_blank">
                        <v-icon>mdi-eye</v-icon>
                    </v-btn>
                    <v-btn @click="remove(item.id)">
                        <v-icon>mdi-delete</v-icon>
                    </v-btn>
                </v-btn-toggle>
            </template>
            <template #item.subscribe="{ item }">
                <v-checkbox v-model="item.subscribe"
                            @change="changeSubscribe(item.id, item.subscribe)"/>
            </template>
            <template #item.watched="{ item }">
                <v-checkbox v-model="item.watched"
                            @change="changeWatch(item.id, item.watched)"/>
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
                crudApiEndpoint: '/api/profiles',
                newProfileUrl: '',
                headers: [
                    {text: this.$t('id'), value: 'id', width: '2%'},
                    {value: 'picture', width: "100px", sortable: false},
                    {text: this.$t('Name'), value: 'name'},
                    {text: this.$t('Account'), value: 'socNetwork', sortable: false},
                    {text: this.$t('Last publish'), value: 'last_publish'},
                    {text: this.$t('Saved posts'), value: 'total_posts'},
                    {value: 'url', sortable: false},
                    {text: this.$t('Subscribed'), value: 'subscribe', type: 'boolean', align:"center", width: '2%'},
                    {text: this.$t('Watched'), value: 'watched', width: '2%'}
                ],
                valid: false,
                requestErrors: '',
            }
        },
        methods: {
            changeWatch ($id, $watched) {
                axios.post(this.crudApiEndpoint + "/watch/" + $id + "/" + $watched);
            },
            changeSubscribe($id, $subscribed) {
                axios.post(this.crudApiEndpoint + "/subscribe/" + $id + "/" + $subscribed);
            },
            add() {
                this.loading = true
                axios.post(this.crudApiEndpoint + "/add", {'url' : this.newProfileUrl})
                .then(() => {this.success()})
                .catch(error => this.catchFail(error));
            },
            catchFail(error) {
                this.loading = false
                this.requestErrors = error.response.data
            },
            success() {
                this.newProfileUrl = ""
                this.fetch()
                this.valid = true
            },
            indicateSite($url) {
                return ($url.includes('facebook') ? 'facebook' :
                    $url.includes('instagram') ? 'instagram' :
                        $url.includes('twitter') ? 'twitter' : '')
            },
            remove($id) {
                this.loading = true
                axios.post(this.crudApiEndpoint + "/remove/" + $id)
                    .then(x => this.fetch())
            },
        },
        computed: {
            validate() {
                let value = this.newProfileUrl
                if (! /([-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)|(^$))/.test(value))
                    return this.$t('Enter a valid URL')
                if(! (value === '' || value.includes('facebook.com/') || value.includes('instagram.com/') || value.includes('twitter.com/'))) {
                    return this.$t('Link must lead to a profile');
                }
                if( this.requestErrors !== '')
                    if(this.requestErrors === 'Already in db')
                        this.search = this.newProfileUrl
                    return this.$t(this.requestErrors)
                return ''
            }
        }
    }
</script>

