<template>
    <div v-if="!isVideo" v-show="this.show">
        <div class="d-inline-flex" v-if="images[0] && !images[0].includes(`https://instagram`)">
            <img class="image" v-for="(image, i) in images" v-if="i<2"
                 :src="image" :key="i" @click="index = i" style="object-fit: cover; height: 100px; width: 100px"
                 >
            <span class="my-auto" v-else-if="i===2">+</span>
        </div>
        <template>
            <vue-gallery-slideshow :images="images" :index="index" @close="index = null" @error="placeholder"/>
        </template>
    </div>
    <div v-else>
        <video :src="images[0]" style="max-width: 150px; max-height: 150px" controls/>
    </div>
</template>

<script>
    import VueGallerySlideshow from 'vue-gallery-slideshow';

    export default {
        name: "GalleryComponent",
        components: {
            VueGallerySlideshow,
        },
        data() {
            return {
                index: null,
                isVideo: false,
                show: false
            }
        },
        props: {
            images: {
                default: [],
            },
        },
        methods: {
            testIfSingle(e) {
                if(this.images.length===1) {
                    this.isVideo = true
                } else {
                    let idx = this.images.indexOf(e.target.src)
                    this.images[idx] = "images/video_placeholder.jpg"
                    e.target.src = "images/video_placeholder.jpg"
                }
            },
            placeholder(e) {
                e.target.src = "images/video_placeholder.jpg"
            },
            validateImages() {
                let succeeded = 0
                this.images.forEach((img, i) => {
                    if(img.includes("https://instagram")) {
                        $.get(`/api/image/?url=${this.urlEncode(img)}`)
                            .then(response => {
                                this.images[i] = `data:image/png;base64, ${response}`;
                                succeeded++
                                if(succeeded === this.images.length) {
                                    this.$nextTick(() => {
                                        this.show = true
                                    });
                                }
                            })
                    }
                    else {
                        this.images[i] = img
                        this.show = true
                    }
                });
            },
            urlEncode($str) {
                return encodeURIComponent($str)
                    .replace('!', '%21')
                    .replace('\'', '%27')
                    .replace('(', '%28')
                    .replace(')', '%29')
                    .replace('*', '%2A')
                    .replace('%20', '+');
            }
        },
        created() {
            this.validateImages()
        }
    }
</script>
