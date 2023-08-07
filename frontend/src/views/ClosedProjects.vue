<template>
    <div class="py-4 container-fluid">
      <div class="row">
        <div class="col-12">
          <closed-projects-table type-prop="Kapandı" filter="0"/>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ClosedProjectsTable from "@/views/components/ClosedProjectsTable.vue";
  export default {
    name: "ClosedProjectsPage",
    components: {
      ClosedProjectsTable,
    },
  };
  </script>
  