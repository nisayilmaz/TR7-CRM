<style>
  a {
      cursor: pointer;
  }
</style>
<template>
  <div class="nav-wrapper position-relative end-0">
    <ul class="nav nav-pills nav-fill p-1" role="tablist">
      <li class="nav-item">
        <a @click="setFilter(0)"
          class="nav-link mb-0 px-0 py-1 active active"
          role="tab"
          aria-selected="true"
          >Tüm Notlar</a
        >
      </li>
      <li class="nav-item">
        <a @click="setFilter(1)"
          class="nav-link mb-0 px-0 py-1"
          role="tab"
          aria-selected="false"
          >Arama</a
        >
      </li>
      <li class="nav-item">
        <a @click="setFilter(2)"
          class="nav-link mb-0 px-0 py-1"
          role="tab"
          aria-selected="false"
          >Yüzyüze Görüşme</a
        >
      </li>
      <li class="nav-item">
        <a @click="setFilter(3)"
          class="nav-link mb-0 px-0 py-1"
          role="tab"
          aria-selected="false"
          >İş Ortağı İle Görüşme</a
        >
      </li>
        <li class="nav-item">
            <a @click="setFilter(4)"
                  class="nav-link mb-0 px-0 py-1"
                  role="tab"
                  aria-selected="false"
            >E-posta</a
            >
        </li>
        <li class="nav-item">
            <a @click="setFilter(5)"
                  class="nav-link mb-0 px-0 py-1"
                  role="tab"
                  aria-selected="false"
            >Genel</a
            >
        </li>
        <li class="nav-item">
            <a @click="setFilter(6)"
                  class="nav-link mb-0 px-0 py-1"
                  role="tab"
                  aria-selected="false"
            >Etkinlik</a
            >
        </li>
        <li class="nav-item">
            <a @click="setFilter(7)"
                  class="nav-link mb-0 px-0 py-1"
                  role="tab"
                  aria-selected="false"
            >İş Yemeği</a
            >
        </li>
        <li class="nav-item">
            <a @click="setFilter(8)"
                  class="nav-link mb-0 px-0 py-1"
                  role="tab"
                  aria-selected="false"
            >Diğer</a
            >
        </li>
    </ul>
  </div>
</template>
<script>
import setNavPills from "@/assets/js/nav-pills.js";

export default {
  name: "NavPill",
  mounted() {
    setNavPills();
  },
  methods: {
      setFilter(filter) {
          this.$emit('variable-changed', filter);
      }
  }
};
</script>
