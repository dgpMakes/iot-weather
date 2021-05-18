<template>
  <div>
    <h1 class="my-3 center">
      <strong>{{ deviceName }}</strong>
    </h1>
    <table class="table">
      <thead>
        <tr>
          <th scope="col">Date</th>
          <th scope="col">Temperature</th>
          <th scope="col">Humidity</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(m, idx) in displayedDevices" :key="idx">
          <th scope="row">
            <router-link :to="'/device/' + m.device_id">
              {{ m.date }}
            </router-link>
          </th>
          <td>{{ m.temperature }}</td>
          <td>{{ m.humidity }}</td>
        </tr>
      </tbody>
    </table>
    <nav>
      <p style="display: inline">Page {{ page }} of {{ pages.length }}</p>

      <ul class="pagination">
        <li class="page-item">
          <button
            type="button"
            class="page-link d-inline"
            v-if="page > 1"
            @click="page--"
          >
            Previous
          </button>
        </li>
        <li class="page-item">
          <button
            type="button"
            @click="page++"
            v-if="page < pages.length"
            class="page-link d-inline"
          >
            Next
          </button>
        </li>
      </ul>
    </nav>
  </div>
</template>






<script>
export default {
  name: "Measurements",
  data() {
    return {
      posts: [""],
      page: 1,
      perPage: 9,
      pages: [],
    };
  },

  methods: {
    getPosts() {
      fetch("http://localhost:5000/dso/devices/" + this.$route.params.id + "/")
        .then((response) => response.json())
        .then((json) => {
          this.posts = json.data;
        });
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
      let from = page * perPage - perPage;
      let to = page * perPage;
      return posts.slice(from, to);
    },
  },
  computed: {
    displayedDevices() {
      return this.paginate(this.posts);
    },
    deviceName() {
      return this.$route.params.id;
    },
  },
  watch: {
    posts() {
      this.setPages();
    },
  },
  created() {
    this.getPosts();
  },
  filters: {
    trimWords(value) {
      return value.split(" ").splice(0, 20).join(" ") + "...";
    },
  },
};
</script>