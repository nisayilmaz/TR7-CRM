<template>
  <div
    id="sidenav-collapse-main"
    class="w-auto h-auto collapse navbar-collapse max-height-vh-100 h-100"
  >
    <ul class="navbar-nav">
      <li class="nav-item">
        <sidenav-collapse nav-text="Dashboard" :to="{ name: 'Dashboard' }">
          <template #icon>
            <icon name="dashboard" />
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item">
        <sidenav-collapse nav-text="Kurumlar" :to="{ name: 'Companies' }">
          <template #icon>
            <icon name="tables" />
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item">
        <sidenav-collapse nav-text="İş Ortakları" :to="{ name: 'Partners' }">
          <template #icon>
            <icon name="tables" />
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item">
        <sidenav-collapse nav-text="Kişiler" :to="{ name: 'People' }">
          <template #icon>
            <icon name="customer-support" />
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item">
        <sidenav-collapse nav-text="Fırsatlar" :to="{ name: 'Projects' }">
          <template #icon>
            <icon name="document" />
          </template>
        </sidenav-collapse>
      </li>
        <li class="nav-item">
            <sidenav-collapse nav-text="Gerçekleşen Fırsatlar" :to="{ name: 'FinishedProjects' }">
                <template #icon>
                    <icon name="document" />
                </template>
            </sidenav-collapse>
        </li>
        <li class="nav-item">
            <sidenav-collapse nav-text="Kapanan Fırsatlar" :to="{ name: 'ClosedProjects' }">
                <template #icon>
                    <icon name="document" />
                </template>
            </sidenav-collapse>
        </li>
        <li class="nav-item">
            <sidenav-collapse nav-text="Kaybedilen Fırsatlar" :to="{ name: 'LostProjects' }">
                <template #icon>
                    <icon name="document" />
                </template>
            </sidenav-collapse>
        </li>
        <li v-if="store.state.role === 1" class="nav-item">
        <sidenav-collapse nav-text="Kullanıcılar" :to="{ name: 'Users' }">
          <template #icon>
            <icon name="customer-support" />
          </template>
        </sidenav-collapse>
      </li>
     <!--  <li class="mt-3 nav-item">
        <h6
          class="text-xs ps-4 text-uppercase font-weight-bolder opacity-6"
          :class="$store.state.isRTL ? 'me-4' : 'ms-2'"
        >PAGES</h6>
      </li>
      <li class="nav-item">
        <sidenav-collapse nav-text="Profile" :to="{ name: 'Profile' }">
          <template #icon>
            <icon name="customer-support" />
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item">
        <sidenav-collapse nav-text="Sign In" :to="{ name: 'Sign In' }">
          <template #icon>
            <icon name="sign-in" />
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item">
        <sidenav-collapse nav-text="Sign Up" :to="{ name: 'Sign Up' }">
          <template #icon>
            <icon name="sign-up" />
          </template>
        </sidenav-collapse>
      </li> -->
    </ul>
  </div>
</template>
<script>
import Icon from "@/components/Icon.vue";
import SidenavCollapse from "./SidenavCollapse.vue";
import SidenavCard from "./SidenavCard.vue";
import store from "@/store";

export default {
  name: "SidenavList",
    computed: {
        store() {
            return store
        }
    },
  components: {
    Icon,
    SidenavCollapse,
    SidenavCard,
  },
  props: {
    cardBg: {
      type: String,
      default: ""
    },
  },
  data() {
    return {
      title: "Vite Soft UI Dashboard",
      controls: "dashboardsExamples",
      isActive: "active",
    };
  },
  methods: {
    getRoute() {
      const routeArr = this.$route.path.split("/");
      return routeArr[1];
    },
  },
};
</script>
