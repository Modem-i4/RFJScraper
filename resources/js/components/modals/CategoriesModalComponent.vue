<template>
    <div>
        <template v-for="(el, index) in item.categories">
            <template v-if="item.categories[index] !== null">
                <v-autocomplete
                    v-model="item.categories[index]"
                    append-icon=""
                    :items="categories.filter( el => {
                        if((!item.categories.includes(el.id) && el.display) || el.id === item.categories[index])
                             return el
                    } )"
                    item-text="name"
                    item-value="id"
                    clearable
                    dense
                    @change="update(item.id, item.categories); newCategory = '';
                    () => {if(item.categories[index]==='') item.categories[index] = null}"
                />
            </template>
        </template>
        <div>
            <v-autocomplete
                v-model="newCategory"
                :items="this.categories.filter( el => {
                        if((!this.item.categories.includes(el.id) && el.display))
                            return el
                    } )"
                @change="addCategory"
                item-text="name"
                item-value="id"
                label="Add to a category"
                dense
            />
        </div>
    </div>
</template>


<script>
export default {
    name: "TextModalComponent",
    data() {
        return {
            newCategory: null,
            crudApiEndpoint: '/api/posts',
        }
    },
    props: {
        item: {
            default: {},
        },
        categories: {
            default: [],
        }
    },
    methods: {
        addCategory() {
            this.item.categories.push(this.newCategory)
            this.error = ''
            this.newCategory=null
            this.update(this.item.id, this.item.categories)
        },
        update($id, $categories) {
            this.item.categories = this.item.categories.filter($item => $item !== null)
            axios.post(this.crudApiEndpoint + "/categories/" + $id, {'categories': $categories});
        }
    }
}
</script>
