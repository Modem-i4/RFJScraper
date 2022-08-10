<template>
    <v-menu
        :close-on-content-click="false"
        origin="center center"
        transition="scale-transition"
        style="max-width: 50%"
        v-model="isOpen"
    >
        <template #activator="{ on, attrs }">
            <div class="text-table-el"
                 v-html="value"
                 v-bind="attrs"
                 v-on="on"/>
        </template>

        <div class="bg-white">
            <v-icon class="float-right"
                    @click="isOpen=false"
            >mdi-close</v-icon>
            <div v-html="value" class="container"/>
        </div>
    </v-menu>
</template>


<script>
export default {
    name: "TextModalComponent",
    data() {
        return {
            isOpen: false,
        }
    },
    props: {
        value: {
            default: 0,
        },
    }
}
</script>
