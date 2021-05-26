<template>
  <div>
    <h1 class="my-3 center">
      <strong>{{ deviceName }}</strong>
    </h1>

    <div class="d-flex">
      <div class="date-picker">
        <h5>Date Picker</h5>

        <v-date-picker
          v-model="range"
          mode="dateTime"
          :masks="masks"
          is-range
        />
      </div>

      <div class="measurements-table">
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
                {{ m.date }}
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
    </div>
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
      timer: "",
      date1: new Date("DD-MM-YYYY hh:mm:ss"),
      date2: new Date("DD-MM-YYYY hh:mm:ss"),
      range: {
        start: new Date(2020, 0, 6),
        end: new Date(2020, 0, 23),
      },
      masks: {
        input: "DD-MM-YYYY hh:mm",
      },
    };
  },

  methods: {
    getPosts() {
      fetch(
        "http://weatherstation.tk:5000/dso/devices/" +
          this.$route.params.id +
          "?start=" +
          this.range.start +
          "&end=" +
          this.range.end
      )
        .then((response) => response.json())
        .then((json) => {
          this.posts = json.data;
        });
    },
    setPages() {
      let numberOfPages = Math.ceil(this.posts.length / this.perPage);
      this.pages = [];
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
    this.timer = setInterval(this.getPosts, 2000);
  },
  filters: {
    trimWords(value) {
      return value.split(" ").splice(0, 20).join(" ") + "...";
    },
  },
};
</script>

<style>
.measurements-table {
  flex: 1;
}

.date-picker {
  flex: 0;
  margin-top: 10px;
  margin-right: 30px;
}
</style>