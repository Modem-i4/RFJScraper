
export default {
    data() {
        return {
            pagination: {},
            search: '',
            searches:{},
            items: [],
            newItem: {},

            loading: true,
            options: {
                itemsPerPage: 10,
                sortDesc : 'desc',
            },
            footerOptions: {
                itemsPerPageOptions: [10, 25, 50, 100],
            },

            crudApiEndpoint: '',
            headers: [],
            defaultSortByField: 'id',
            defaultSortDirection: 'desc',
        }
    },
    computed: {
        sortBy() {
            if (this.options.sortBy.length === 0) {    // If no column is selected for sorting, return the default value
                return this.defaultSortByField;
            }
            return this.options.sortBy[0];
        },
        sortDirection() {
            if(this.options.sortDesc[0] === 'd') {
                return this.defaultSortDirection;
            }
            return this.sortBy == null ? null : this.options.sortDesc[0] ? 'asc' : 'desc';
        },
    },
    watch: {
        options: {
            handler() {
                this.fetch()
            },
            deep: true,
        },
        search: _.debounce(function () {
            this.applySearch()

        }, 400),
        searches: {
            handler() {
                this.applySearch()
            },
            deep: true,
        }
    },
    methods: {
        applySearch() {
            this.options.page = 1;
            this.fetch()
        },
        fetch() {
            this.loading = true;
            axios.get(this.crudApiEndpoint, {
                params: {
                    search: (this.search === '' ? null : this.search),
                    searches: this.searches,

                    page: this.options.page,
                    perPage: this.options.itemsPerPage,

                    sortBy: this.sortBy,
                    sortDirection: this.sortDirection,
                }
            }).then(response => {
                this.items = response.data.data;
                console.log(this.items)
                this.pagination.total = response.data.total;

                this.loading = false;
            })
        },
    }
}
