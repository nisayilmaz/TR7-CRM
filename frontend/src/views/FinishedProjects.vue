<template>
    <div class="py-4 container-fluid">
      <div class="row">
        <div class="col-12">
          <finished-projects-table />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import ProjectsTable from "./components/ProjectsTable.vue";
  import FinishedProjectsTable from "@/views/components/FinishedProjectsTable.vue";
  
  export default {
    name: "ProjectsPage",
    components: {
      FinishedProjectsTable
    },
  };
  </script>
  