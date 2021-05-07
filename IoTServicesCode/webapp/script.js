const app = new Vue({
    el: '#app',
    data() {
        return {
            posts: [''],
            page: 1,
            perPage: 9,
            pages: [],
        }
    },

    methods: {
        getPosts() {
            var data;
            fetch("http://api.uc3m.tk:5000/dso/measurements")
                .then(response => response.json())
                .then(json => { this.posts = json.data }
                );
        },
        setPages() {
            let numberOfPages = Math.ceil(this.posts.length / this.perPage);
            for (let index = 1; index <= numberOfPages; index++) {
                this.pages.push(index);
            }
        },
        paginate(posts) {
            let page = this.page;
            let perPage = this.perPage;
            let from = (page * perPage) - perPage;
            let to = (page * perPage);
            return posts.slice(from, to);
        }
    },
    computed: {
        displayedMeasurements() {
            return this.paginate(this.posts);
        }
    },
    watch: {
        posts() {
            this.setPages();
        }
    },
    created() {
        this.getPosts();
    },
    filters: {
        trimWords(value) {
            return value.split(" ").splice(0, 20).join(" ") + '...';
        }
    }
})