<template>
  <div class="progress">
    <div
      class="progress-bar"
      :style="{ width: percentage + '%', backgroundColor: getColor(percentage) + ' !important' }"
    ></div>
  </div>
</template>

<script>
export default {
  name: "VsudProgress",
  props: {
    percentage: {
      type: String,
      default: ""
    },
  },
  methods: {
    getColor: (percentage) => {
      let colorValue;

      if (percentage <= 15) {
        colorValue = "#cc3300";
      }
      else if (percentage > 15 && percentage <= 25) {
          colorValue = "#ff6700";
      }
      else if (percentage > 25 && percentage <= 50) {
          colorValue = "#ffcc00";
      }
      else if (percentage > 50 && percentage <= 75) {
          colorValue = "#99cc33";
      }
      else{
          colorValue = "#339900";
      }

      return `${colorValue}`;
    },
  },
};
</script>