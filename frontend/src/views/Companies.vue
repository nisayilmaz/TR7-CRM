<template>
  <div class="py-4 container-fluid">
    <div class="row">
      <div class="col-12">
        <companies-table type="client" />
      </div>
    </div>
  </div>
</template>

<script>
import CompaniesTable from "./components/CompaniesTable.vue";

export default {
  name: "CompaniesPage",
  components: {
    CompaniesTable,
  },
};
</script>
