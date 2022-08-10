<template>
    <v-app>
        <v-card-title>
            <h2>{{$t('Posts')}}</h2>
            <v-btn-toggle rounded class="ml-5">
                <v-btn small :color="soc_network_filter === filter_patterns.fb ? '#1976d2':''"
                       @click="soc_network_filter = soc_network_filter === filter_patterns.fb ? '' : filter_patterns.fb; searches['base.url'] = soc_network_filter; applySearch()">
                    <v-icon small :color="soc_network_filter === filter_patterns.fb ? 'white' : ''">
                        mdi-facebook
                    </v-icon>
                </v-btn>
                <v-btn small :color="soc_network_filter === filter_patterns.insta ? '#1976d2':''"
                       @click="soc_network_filter = soc_network_filter === filter_patterns.insta ? '' : filter_patterns.insta; searches['base.url'] = soc_network_filter; applySearch()">
                    <v-icon small :color="soc_network_filter === filter_patterns.insta ? 'white' : ''">
                        mdi-instagram
                    </v-icon>
                </v-btn>
                <v-btn small :color="soc_network_filter === filter_patterns.twitter ? '#1976d2':''"
                       @click="soc_network_filter = soc_network_filter === filter_patterns.twitter ? '' : filter_patterns.twitter; searches['base.url'] = soc_network_filter; applySearch()">
                    <v-icon small :color="soc_network_filter === filter_patterns.twitter ? 'white' : ''">
                        mdi-twitter
                    </v-icon>
                </v-btn>
            </v-btn-toggle>
            <v-spacer></v-spacer>
            <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                :label="this.$t('Search')"
                single-line
                hide-details
                clearable
                autocomplete="nope"
            ></v-text-field>
        </v-card-title>
        <v-data-table
            :footer-props="footerOptions"
            :headers="headers"
            :items="items"
            :options.sync="options"
            :server-items-length="pagination.total"
            :loading="loading"
            :search="search"
        >
            <template #header.name="{ header }">
                <v-text-field :label="header.text"
                              v-model="searches[header.text]"
                              dense
                              clearable
                              autocomplete="nope"
                              @click:clear="searches[header.text] = '';applySearch()"/>
            </template>
            <template #header.text="{ header }">
                <v-text-field :label="header.text"
                              v-model="searches[header.text]"
                              dense
                              clearable
                              autocomplete="nope"
                              @click:clear="searches[header.text] = '';applySearch()"/>
            </template>
            <template #header.categories="{ header }">
                <v-autocomplete :label="header.text"
                                v-model="searches[header.text]"
                                text
                                item-text="name"
                                item-value="id"
                                clearable
                                autocomplete="nope"
                                dense
                                :items="categories.filter( el => el.display)"
                />
            </template>
            <template #header.view="{ header }">
                <div class="mx-auto" style="display: table;">
                <v-btn-toggle rounded>
                    <v-btn small :color="status_filter === 'edit' ? '#1976d2':''"
                           @click="status_filter = status_filter === 'edit' ? '' : 'edit'; searches.status = status_filter; applySearch()">
                        <v-icon small :color="status_filter === 'edit' ? 'white' : ''">
                            mdi-pencil
                        </v-icon>
                    </v-btn>
                    <v-btn small :color="status_filter === 'delete' ? '#1976d2':''"
                           @click="status_filter = status_filter === 'delete' ? '' : 'delete'; searches.status = status_filter; applySearch()">
                        <v-icon small :color="status_filter === 'delete' ? 'white' : ''">
                            mdi-delete
                        </v-icon>
                    </v-btn>
                </v-btn-toggle>
                </div>
            </template>
            <template #header.important="{ header }">
                <v-checkbox v-model="searches[header.text]"/>
            </template>


            <template #item.picture_url="{ item }">
                <a :href="item.profile_url" target="_blank">
                    <v-img :src="item.is_group ? `/images/group.jpg` :
                    `/images/profiles/${item.profile_id}.jpg`" :alt="item.picture_url" max-width="70px"/>
                </a>
            </template>
            <template #item.name="{ item }">
                <a @click="searches.Name=item.name; applySearch()">
                    <span>{{ item.name }}</span>
                    <v-icon small>mdi-{{indicateSite(item.url)}}</v-icon>
                </a>
            </template>
            <template #item.text="{ value }">
                <text_modal_component
                :value="value"/>
            </template>
            <template #item.images="{ value }">
                <gallery_component
                    :images="value !== null ? value : []" @error="alert(`gallery error`)"/>
            </template>
            <template #item.categories="{ item }">
                <categories_component
                    :item="item"
                    :categories="categories"
                />
            </template>
            <template #item.view="{ item }">
                <v-btn-toggle
                :background-color="getBtnBackground(item.status)">
                    <v-btn :href="item.url" target="_blank">
                        <v-icon>mdi-eye</v-icon>
                    </v-btn>
                    <v-btn :href="`/posts/${item.id}`" target="_blank">
                        <v-icon>mdi-hammer-wrench</v-icon>
                    </v-btn>
                    <v-btn @click="searches={}; search=item.url"
                           v-if="item.status==='edited'||item.status==='edited_to'||item.status==='deleted_after_edit'">
                        <v-icon>mdi-link-variant</v-icon>
                    </v-btn>
                    <v-btn v-else @click="remove(item.id)">
                        <v-icon>mdi-delete</v-icon>
                    </v-btn>
                </v-btn-toggle>
            </template>
            <template #item.important="{ item }">
                <v-checkbox v-model="item.important"
                @change="changeImportance(item.id, item.important)"/>
            </template>
        </v-data-table>
    </v-app>
</template>

<script>
    import TextModalComponent from "./modals/TextModalComponent";
    import DataTableCore from "../mixins/DataTableCore";
    import GalleryComponent from "./modals/GalleryComponent";
    import CategoriesComponent from "./modals/CategoriesModalComponent";

    export default {
        mixins: [DataTableCore],
        components: {
            'text_modal_component': TextModalComponent,
            'gallery_component': GalleryComponent,
            'categories_component': CategoriesComponent,
        },
        data () {
            return {
                crudApiEndpoint: '/api/posts',
                categories: [],
                status_filter: '',
                soc_network_filter: '',
                filter_patterns: {
                    fb: "https://www.facebook.com/",
                    insta: "https://www.instagram.com/",
                    twitter: "https://twitter.com/"
                },
                headers: [
                    {text: this.$t('id'), value: 'id', width: '1%'},
                    {text: this.$t('profile'), value: 'picture_url', width:"1%", sortable: false},
                    {text: this.$t('Name'), value: 'name', width: "15%", sortable: false},
                    {text: this.$t('Text'), value: 'text', width: "40%", sortable: false},
                    {text: this.$t('Images'), value: 'images', width: "210px", sortable: false},
                    {text: this.$t('Date'), value: 'published_at', width: "10%"},
                    {text: this.$t('Categories'), value: 'categories', width: "20%", sortable: false},
                    {value: 'view', width: "1%", sortable: false},
                    {text: this.$t('Important'), value: 'important', type: 'boolean', align:"center", width: '2%', sortable: false},
                ],
            }
        },
        methods: {
            changeImportance($id, $importance) {
                axios.post(this.crudApiEndpoint + "/imp/" + $id + "/" + $importance);
            },
            indicateSite($url) {
                return ($url.includes('facebook') ? 'facebook' :
                        $url.includes('instagram') ? 'instagram' :
                        $url.includes('twitter') ? 'twitter' : '')
            },
            getBtnBackground($status) {
                return ($status === 'deleted' || $status === 'deleted_after_edit' ? 'red' :
                        $status === 'edited' ? 'yellow' :
                        $status === 'edited_to' ? 'green' : '')
            },
            getCategories() {
                axios.get("/api/categories/names")
                .then(response => {
                    this.categories = response.data
                })
            },
            remove($id) {
                this.loading = true
                axios.post(this.crudApiEndpoint + "/remove/" + $id)
                .then(x => this.fetch())
            }
        },
        mounted() {
            this.getCategories()
        },
    }
</script>
<style>
    .image {
        cursor: pointer;
    }
    .text-table-el {
        overflow: hidden;
        height: 100px;
    }
    .v-application--is-ltr .v-text-field .v-label {
        transform-origin: top left;
        font-size: 0.75rem;
    }
</style>
