<template>
  <nav
    v-bind="$attrs"
    id="navbarBlur"
    class="shadow-none navbar navbar-main navbar-expand-lg border-radius-xl"
    data-scroll="true"
  >
    <div class="px-3 py-1 container-fluid">
      <breadcrumbs :current-page="currentRouteName" :text-white="textWhite" />
      <div
        id="navbar"
        class="mt-2 collapse navbar-collapse mt-sm-0 me-md-0 me-sm-4"
        :class="$store.state.isRTL ? 'px-0' : 'me-sm-4'"
      >
        <div
          class="pe-md-3 d-flex align-items-center"
          :class="$store.state.isRTL ? 'me-md-auto' : 'ms-md-auto'"
        >
        </div>
        <ul class="navbar-nav justify-content-end">
          <li class="nav-item d-xl-none px-2 d-flex align-items-center">
            <a
              id="iconNavbarSidenav"
              class="p-0 nav-link text-body"
              @click="toggleSidebar"
            >
              <div class="sidenav-toggler-inner">
                <i class="sidenav-toggler-line"></i>
                <i class="sidenav-toggler-line"></i>
                <i class="sidenav-toggler-line"></i>
              </div>
            </a>
          </li>
<!--          <li class="px-3 nav-item d-flex align-items-center">-->
<!--            <a-->
<!--              class="p-0 nav-link"-->
<!--              :class="textWhite ? textWhite : 'text-body'"-->
<!--              @click="toggleConfigurator"-->
<!--            >-->
<!--              <i class="cursor-pointer fa fa-cog fixed-plugin-button-nav"></i>-->
<!--            </a>-->
<!--          </li>-->
            <li class="me-2">
                <span class=" text-xs font-weight-bold">{{$store.state.name}}</span>
            </li>
          <li
            class="ms-2 nav-item dropdown d-flex align-items-center"
          >
            <a
              id="dropdownMenuButton"
              href="#"
              class="p-0 nav-link"
              :class="[
                textWhite ? textWhite : 'text-body',
                showMenu ? 'show' : '',
              ]"
              data-bs-toggle="dropdown"
              aria-expanded="false"
              @click="showMenu = !showMenu"
            >
              <i class="fa fa-user me-sm-1" ></i>
            </a>
            <ul
              class="px-2 py-3 dropdown-menu dropdown-menu-end me-sm-n4"
              :class="showMenu ? 'show' : ''"
              aria-labelledby="dropdownMenuButton"
            >
              <li class="mb-2">

                <a @click="logout" style="cursor: pointer" class="dropdown-item border-radius-md">
                  <div class="py-1 d-flex">

                    <div class="d-flex flex-column justify-content-center">
                      <h6 class="mb-1 text-sm font-weight-normal">
                       Çıkış Yap
                      </h6>
<!--                      <p class="mb-0 text-xs text-secondary">-->
<!--                        <i class="fa fa-clock me-1"></i>-->
<!--                        13 minutes ago-->
<!--                      </p>-->
                    </div>
                  </div>
                </a>
              </li>
              <li class="mb-2">
                <a class="dropdown-item border-radius-md" href="javascript:;">
                  <div class="py-1 d-flex">

                    <div class="d-flex flex-column justify-content-center">
                      <h6 class="mb-1 text-sm font-weight-normal">
                       Parola Değiştir
                      </h6>
<!--                      <p class="mb-0 text-xs text-secondary">-->
<!--                        <i class="fa fa-clock me-1"></i>-->
<!--                        1 day-->
<!--                      </p>-->
                    </div>
                  </div>
                </a>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
<script>
import Breadcrumbs from "../Breadcrumbs.vue";
import { mapMutations, mapActions } from "vuex";
import {axiosInstance} from "@/utils/utils";

export default {
  name: "NavbarComponent",

  components: {
    Breadcrumbs,
  },
  props: {
    minNav: {
      type: Function,
      default: () => { }
    },
    textWhite: {
      type: String,
      default: ""
    },
  },
  data() {
    return {
      showMenu: false,
    };
  },
  computed: {
    currentRouteName() {
      return this.$route.name;
    },
  },
  created() {
    this.minNav;
  },
  updated() {
    const navbar = document.getElementById("navbarBlur");
    window.addEventListener("scroll", () => {
      if (window.scrollY > 10 && this.$store.state.isNavFixed) {
        navbar?.classList.add("blur");
        navbar?.classList.add("position-sticky");
        navbar?.classList.add("shadow-blur");
      } else {
        navbar?.classList.remove("blur");
        navbar?.classList.remove("position-sticky");
        navbar?.classList.remove("shadow-blur");
      }
    });
  }, methods: {
    ...mapMutations(["navbarMinimize", "toggleConfigurator"]),
    ...mapActions(["toggleSidebarColor"]),
      async logout(e) {
          e.preventDefault();
          let request = await axiosInstance.post(`/auth/logout/`, null);
          if(request.status === 204) {
              localStorage.removeItem("accessToken");
              this.$router.push('/log-in')
              this.$store.state.role = "";
          }
      },

    toggleSidebar() {
      this.toggleSidebarColor("bg-white");
      this.navbarMinimize();
    },
  },
};
</script>
