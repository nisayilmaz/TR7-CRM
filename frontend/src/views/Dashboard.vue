<template>
  <div class="py-4 container-fluid">
      <div class="row mb-4">
          <div class="col-xl-6 col-sm-6 mb-xl-0 mb-4">
              <default-info-card
                      icon-bg="bg-gradient-danger"
                      title="Aktif Fırsatlar Tahmini Gelir"
                      class-icon="fa-solid fa-sack-dollar"
                      :price="total_budget.toString() + '$'"/>
          </div>
          <div class="col-xl-6 col-sm-6 mb-xl-0 mb-4">
              <default-info-card
                      icon-bg="bg-gradient-yellow"
                      title="Kazanılan Anlaşmaların Toplam Değeri"
                      class-icon="fa-solid fa-trophy"
                      :price="total_sold.toString() + '$'"/>
          </div>
      </div>
    <div class="row">
        <div class="col-xl-3 col-sm-6 mb-xl-0 mb-2">
            <card
                    :title="'Toplam Fırsat Sayısı'"
                    :value="project_cnt.toString()"
                    :icon-class="'fas fa-tasks'"
                    :icon-background="'bg-gradient-secondary'"
                    direction-reverse
            ></card>
        </div>
        <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
            <card
                    :title="'Gerçekleşen Fırsat Sayısı'"
                    :value="fin_cnt.toString()"
                    :icon-class="'fas fa-tasks'"
                    :icon-background="'bg-gradient-warning'"
                    direction-reverse
            ></card>
        </div>
        <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
            <card
                    :title="'Kurum Sayısı'"
                    :value="client_cnt.toString()"
                    :icon-class="'far fa-building'"
                    :icon-background="'bg-gradient-success'"
                    direction-reverse
            ></card>
        </div>
      <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
        <card
          :title="'İş Ortağı Sayısı'"
          :value="partner_cnt.toString()"
          :icon-class="'far fa-building'"
          :icon-background="'bg-gradient-primary'"
          direction-reverse
        ></card>
      </div>

<!--      <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
        <card
          :title="stats.users.title"
          :value="stats.users.value"
          :percentage="stats.users.percentage"
          :icon-class="stats.users.iconClass"
          :icon-background="stats.iconBackground"
          direction-reverse
        ></card>
      </div>
      <div class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
        <card
          :title="stats.clients.title"
          :value="stats.clients.value"
          :percentage="stats.clients.percentage"
          :icon-class="stats.clients.iconClass"
          :icon-background="stats.iconBackground"
          :percentage-color="stats.clients.percentageColor"
          direction-reverse
        ></card>
      </div>-->
    </div>

<!--    <div class="row">-->
<!--      <div class="col-lg-7 mb-lg-0 mb-4">-->
<!--        <div class="card">-->
<!--          <div class="card-body p-3">-->
<!--            <div class="row">-->
<!--              <div class="col-lg-6">-->
<!--                <div class="d-flex flex-column h-100">-->
<!--                  <p class="mb-1 pt-2 text-bold">Built by developers</p>-->
<!--                  <h5 class="font-weight-bolder">Vite Soft UI Dashboard</h5>-->
<!--                  <p class="mb-5">-->
<!--                    From colors, cards, typography to complex elements, you will-->
<!--                    find the full documentation.-->
<!--                  </p>-->
<!--                  <a-->
<!--                    class="text-body text-sm font-weight-bold mb-0 icon-move-right mt-auto"-->
<!--                    href="javascript:;"-->
<!--                  >-->
<!--                    Read More-->
<!--                    <i-->
<!--                      class="fas fa-arrow-right text-sm ms-1"-->
<!--                      aria-hidden="true"-->
<!--                    ></i>-->
<!--                  </a>-->
<!--                </div>-->
<!--              </div>-->
<!--              <div class="col-lg-5 ms-auto text-center mt-5 mt-lg-0">-->
<!--                <div class="bg-gradient-success border-radius-lg h-100">-->
<!--                  <img-->
<!--                    src="../assets/img/shapes/waves-white.svg"-->
<!--                    class="position-absolute h-100 w-50 top-0 d-lg-block d-none"-->
<!--                    alt="waves"-->
<!--                  />-->
<!--                  <div-->
<!--                    class="position-relative d-flex align-items-center justify-content-center h-100"-->
<!--                  >-->
<!--                    <img-->
<!--                      class="w-100 position-relative z-index-2 pt-4"-->
<!--                      src="../assets/img/illustrations/rocket-white.png"-->
<!--                      alt="rocket"-->
<!--                    />-->
<!--                  </div>-->
<!--                </div>-->
<!--              </div>-->
<!--            </div>-->
<!--          </div>-->
<!--        </div>-->
<!--      </div>-->
<!--      <div class="col-lg-5">-->
<!--        <div class="card h-100 p-3">-->
<!--          <div-->
<!--            class="overflow-hidden position-relative border-radius-lg bg-cover h-100"-->
<!--            style="-->
<!--              background-image: url('https://demos.creative-tim.com/soft-ui-dashboard/assets/img/ivancik.jpg');-->
<!--            "-->
<!--          >-->
<!--            <span class="mask bg-gradient-dark"></span>-->
<!--            <div-->
<!--              class="card-body position-relative z-index-1 d-flex flex-column h-100 p-3"-->
<!--            >-->
<!--              <h5 class="text-white font-weight-bolder mb-4 pt-2">-->
<!--                Work with the rockets-->
<!--              </h5>-->
<!--              <p class="text-white">-->
<!--                Wealth creation is an evolutionarily recent positive-sum game.-->
<!--                It is all about who take the opportunity first.-->
<!--              </p>-->
<!--              <a-->
<!--                class="text-white text-sm font-weight-bold mb-0 icon-move-right mt-auto"-->
<!--                href="javascript:;"-->
<!--              >-->
<!--                Read More-->
<!--                <i-->
<!--                  class="fas fa-arrow-right text-sm ms-1"-->
<!--                  aria-hidden="true"-->
<!--                ></i>-->
<!--              </a>-->
<!--            </div>-->
<!--          </div>-->
<!--        </div>-->
<!--      </div>-->
<!--    </div>-->
      <div class="row mb-4">
          <vsud-button color="white" class="col-11 ms-5" @click="downloadSummary">
              ÖZET İNDİR
          </vsud-button>
      </div>
    <div class="mt-2 row">
      <div class="mb-4 col-lg-5 mb-lg-0">
        <div class="card z-index-2">
            <div class="pb-0 card-header">
                <h6>Kayıt Özeti</h6>
            </div>
          <div class="p-3 card-body">
            <!-- chart -->
            <active-users-chart :graph-data="barGraphData"/>
          </div>
        </div>
      </div>
      <div class="col-lg-7">
        <!-- line chart -->
        <div class="card z-index-2">
          <gradient-line-chart :graph-data="graphData"/>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Card from "@/examples/Cards/Card.vue";
import ActiveUsersChart from "@/examples/Charts/ActiveUsersChart.vue";
import GradientLineChart from "@/examples/Charts/GradientLineChart.vue";
import OrdersCard from "./components/OrdersCard.vue";
import ProjectsCard from "./components/ProjectsCard.vue";
import DefaultInfoCard from "@/examples/Cards/DefaultInfoCard.vue";

import axios from "axios";
import {axiosInstance} from "@/utils/utils";
import {ca} from "vuetify/locale";
import VsudButton from "@/components/VsudButton.vue";

export default {
  name: "DashboardDefault",
  components: {
      VsudButton,
    Card,
    ActiveUsersChart,
    GradientLineChart,
    ProjectsCard,
    OrdersCard,
    DefaultInfoCard
  },
  computed: {
      graphDataActive() {
          const monthlySales = Array(12).fill(0);
          this.graphData.forEach(entry => {
              if(entry?.count && entry?.month) {
                  monthlySales[entry.month - 1] = entry.count;
              }
          });
          return monthlySales
      }
  },
  data() {
    return {
        projects : [],
        client_cnt: 0,
        fin_cnt: 0,
        partner_cnt: 0,
        project_cnt : 0,
        total_budget: 0,
        total_sold: 0,
        graphData: [],
        barGraphData: [],
    };
  },

    async created() {
        const projectsRes = await axiosInstance.get(`firsatlar`);
        if(projectsRes) {
            this.projects = projectsRes.data.data;
        }

        const statistics = await axiosInstance.get(`/veriler/`);
        if (statistics.data.data) {
            let statisticsData = statistics.data.data
            this.client_cnt = statisticsData?.client_cnt
            this.partner_cnt = statisticsData?.partner_cnt
            this.project_cnt = statisticsData?.project_cnt
            this.fin_cnt = statisticsData?.fin_cnt
            this.graphData = statisticsData?.monthly_sales
            this.barGraphData = statisticsData?.monthly_reg
            if (statisticsData?.total_budget){
              this.total_budget = statisticsData?.total_budget
            }
            if (statisticsData?.total_sold){
                this.total_sold = statisticsData?.total_sold
            }
        }
    },
    methods:{
        async downloadSummary() {
            try{
                const response = await axiosInstance.get("/excel",{
                    responseType: 'blob', // Important: Set the response type to 'blob'

                })

                const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;

                let filename = "ozet.xlsx"
                if (typeof response.headers["content-disposition"] === "string") {
                    let regex = /filename=([^"]+)/.exec((response.headers["content-disposition"]))
                    if(regex) {
                        filename = regex[1]
                    }
                }
                link.setAttribute('download', filename);
                document.body.appendChild(link);
                link.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(link);
            }catch (error) {
                console.error('Error downloading the Excel file:', error);

            }
        },
    }
};
</script>
