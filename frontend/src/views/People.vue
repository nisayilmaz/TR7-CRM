<template>
    <div class="py-4 container-fluid">
      <div class="row">
        <div class="col-12">
          <PeopleTable company_filter="0"/>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import PeopleTable from "./components/PeopleTable.vue";
  
  export default {
    name: "PeoplePage",
    components: {
      PeopleTable,
    },
  };
  </script>
  