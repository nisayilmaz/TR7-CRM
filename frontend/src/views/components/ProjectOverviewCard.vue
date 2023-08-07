<template>
  <div class="card card-blog card-plain">
    <div class="position-relative">
      <a class="shadow-xl d-block border-radius-xl">
      </a>
    </div>
    <div class="px-1 pb-0 card-body">
        <h5>{{ title }}</h5>
          <p>Tarih: {{formatDate(date)}}</p>
      <p class="mb-4 text-sm">
          {{ description }}</p>

    </div>
  </div>
</template>

<script>
import moment from "moment";
export default {
  name: "ProjectsCard",
  props: {
    date: {
      type: String,
    },
    title: {
      type: String,
      default: ""
    },
    description: {
      type: String,
      default: ""
    },
  },
    methods: {
      formatDate(date, format = "DD.MM.YYYY") {
          return moment(date).format(format)
      }
    }
};
</script>
