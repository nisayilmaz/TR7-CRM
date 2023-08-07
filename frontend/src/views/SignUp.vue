<template>
  <navbar   is-blur="blur blur-rounded my-3 py-2 start-0 end-0 mx-4 shadow"
            btn-background="bg-gradient-success"
            :dark-mode="true"/>
  <div class="pt-5 m-3 page-header align-items-start min-vh-50 pb-11 border-radius-lg">

  </div>
  <div class="container">
    <div class="row mt-lg-n10 mt-md-n11 mt-n10 justify-content-center">
      <div class="mx-auto col-xl-4 col-lg-5 col-md-7">
        <div class="card z-index-0">
          <div class="pt-4 text-center card-header">
            <h5>Şifre Sıfırla</h5>
          </div>
          <div class="card-body">
            <form role="form">
                <p v-if="error" class="mb-3"><span class="ms-1 text-bold text-sm" style="color: red">Şifreler uyuşmuyor, lütfen tekrar girin.</span></p>

                <div class="mb-3">
                <vsud-input v-model:value="password" type="password" placeholder="Şifre"  />
              </div>

              <div class="mb-3">
                <vsud-input  v-model:value="repeat_password" type="password" placeholder="Tekrar Şifre"  />
              </div>
                <router-link :to="{ name: 'Dashboard'}"><span class="text-sm text-bold">Giriş Yap</span></router-link>

                <div class="text-center">
                <vsud-button @click="resetPassword" color="dark" full-width variant="gradient" class="my-4 mb-2">Kaydet</vsud-button>
              </div>

            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
<!--  <app-footer />-->
</template>

<script>
import Navbar from "@/examples/PageLayout/Navbar.vue";
import AppFooter from "@/examples/PageLayout/Footer.vue";
import VsudInput from "@/components/VsudInput.vue";
import VsudCheckbox from "@/components/VsudCheckbox.vue";
import VsudButton from "@/components/VsudButton.vue";
import bgImg from "@/assets/img/curved-images/curved6.jpg"
import {noAuthAxiosInstance} from "@/utils/utils";
import Swal from "sweetalert2";
import {th} from "vuetify/locale";
export default {
  name: "SignUp",
  components: {
    Navbar,
    AppFooter,
    VsudInput,
    VsudCheckbox,
    VsudButton,
  },
  data() {
    return {
      bgImg,
        data:"",
        password:"",
        repeat_password:"",
        error : false
    }
  },
  created() {
    this.$store.state.hideConfigButton = true;
    this.$store.state.showNavbar = false;
    this.$store.state.showSidenav = false;
    this.$store.state.showFooter = false;
  },
  beforeUnmount() {
    this.$store.state.hideConfigButton = false;
    this.$store.state.showNavbar = true;
    this.$store.state.showSidenav = true;
    this.$store.state.showFooter = true;
  },
    methods : {
      async resetPassword(e) {
          e.preventDefault()
          this.error = false
          if(this.password === this.repeat_password) {
              try {
                let token = this.$route.params.token
                let response = await noAuthAxiosInstance.post("/auth/password_reset/confirm/",{
                    "token":token,
                    "password":this.password
                })
                Swal.fire(
                    'Şifreniz Başarıyla Sıfırlandı!',
                    '',
                    'success'
                )
                  this.$router.push('/log-in')
              }catch (e) {
                  if(e.response?.data?.detail === "Not found.") {
                      Swal.fire(
                          'Şifreniz Sıfırlanamadı!',
                          "Sıfırlama linkinin süresi dolduğu için şifreniz sıfırlanamadı.",
                          'error'
                      )
                  }
                  else {
                      Swal.fire(
                          'Şifreniz Sıfırlanamadı!',
                          "Şifrenizin en az 8 karakterden oluştuğundan ve sadece rakam içermediğinden emin olun.",
                          'error'
                      )
                  }

              }
          }
          else {
            this.error = true
          }
      }
    }
};
</script>
