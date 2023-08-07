<template>
  <div class="py-4 container-fluid">
    <div class="row">
      <div class="col-12">
        <companies-table type="partner" />
      </div>
    </div>
  </div>
</template>

<script>
import CompaniesTable from "./components/CompaniesTable.vue";

export default {
  name: "PartnersPage",
  components: {
    CompaniesTable,
  },
};
</script>
