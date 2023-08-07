<template>
  <div class="container top-0 position-sticky z-index-sticky">
    <div class="row">
      <div class="col-12">
        <navbar
          is-blur="blur blur-rounded my-3 py-2 start-0 end-0 mx-4 shadow"
          btn-background="bg-gradient-success"
          :dark-mode="true"
        />
      </div>
    </div>
  </div>
  <main class="mt-0 main-content main-content-bg">
    <section>
      <div class="page-header min-vh-75">
        <div class="container">
          <div class="row">
            <div class="mx-auto col-xl-4 col-lg-5 col-md-6 d-flex flex-column">
              <div class="mt-8 card card-plain">
                <div class="pb-0 card-header text-start">
                  <h3 class="font-weight-bolder text-info text-gradient">Hoş Geldiniz</h3>
                  <p v-if="reset_password" class="mb-0">Emailinizi Giriniz.</p>
                  <p v-else class="mb-0">Email ve şifre ile giriş yapınız.</p>
                </div>
                <div class="card-body">
                    <span v-if="error" style="color: red"> Lütfen email ve şifrenizi kontrol edin.</span>

                    <form v-if="reset_password" role="form" class="text-start">
                        <label>Email</label>
                        <vsud-input v-model:value="username" type="email" placeholder="Email" name="email" />
                        <a @click="loginClicked"> <span class="text-sm text-bold"> Giriş Yap </span> </a>
                        <div class="text-center">
                            <vsud-button v-if="!sending" @click="resetPassword"
                                         class="my-4 mb-2"
                                         variant="gradient"
                                         color="info"
                                         full-width
                            >ŞİFRE SIFIRLAMA MAİLİ GÖNDER</vsud-button >
                            <div v-else class="spinner-border mt-3" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                        </div>
                    </form>

                    <form v-else role="form" class="text-start">
                    <label>Email</label>
                    <vsud-input v-model:value="username" type="email" placeholder="Email" name="email" />
                    <label>Şifre</label>
                    <vsud-input v-model:value="password" type="password" placeholder="Şifre" name="password" />
                        <a v-if="!reset_password" @click="resetPasswordClicked"> <span class="text-sm text-bold"> Şifremi Unuttum </span> </a>
                    <div class="text-center">
                      <vsud-button @click="login"
                        class="my-4 mb-2"
                        variant="gradient"
                        color="info"
                        full-width
                      >GİRİŞ YAP</vsud-button >
                    </div>
                  </form>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="oblique position-absolute h-100 d-md-block d-none me-n8">
                <div v-if="$store.state.isDev"
                  class="login-img bg-cover oblique-image position-absolute fixed-top ms-auto h-100 z-index-0 ms-n6"
                  :style="{
                    backgroundImage:
                      `url(${logo})`
                  }"
                ></div>
                  <div v-else
                       class="login-img bg-cover oblique-image position-absolute fixed-top ms-auto h-100 z-index-0 ms-n6"
                       :style="{
                    backgroundImage:
                      `url('/static${logo}')`
                  }"
                  ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script>
import Navbar from "@/examples/PageLayout/Navbar.vue";
import AppFooter from "@/examples/PageLayout/Footer.vue";
import VsudInput from "@/components/VsudInput.vue";
import VsudButton from "@/components/VsudButton.vue";
import bgImg from "@/assets/img/curved-images/curved9.jpg"
import logo from "@/assets/img/tr7_logo_big.png"
import {noAuthAxiosInstance, updateAuth} from "@/utils/utils";
import Swal from "sweetalert2";

const body = document.getElementsByTagName("body")[0];

export default {
  name: "SigninPage",
  components: {
    Navbar,
    AppFooter,
    VsudInput,
    VsudButton,
  },
  data() {
    return {
      bgImg,
      logo,
      username: "",
      password :"",
      error: false,
      reset_password: false,
      sending : false
    }
  },
  beforeMount() {
    this.$store.state.hideConfigButton = true;
    this.$store.state.showNavbar = false;
    this.$store.state.showSidenav = false;
    this.$store.state.showFooter = false;
    body.classList.remove("bg-gray-100");
  },
  beforeUnmount() {
    this.$store.state.hideConfigButton = false;
    this.$store.state.showNavbar = true;
    this.$store.state.showSidenav = true;
    this.$store.state.showFooter = true;
    body.classList.add("bg-gray-100");
  },
    methods: {
        async login(e) {
            e.preventDefault();
            try {
                const response = await noAuthAxiosInstance.post(`/auth/login/`, {
                    username:this.username,
                    password:this.password,
                });
                if(response.data?.token) {
                    window.localStorage.setItem("accessToken", `Token ${response.data.token}`);
                    updateAuth()
                    this.$router.push('/dashboard');
                }
                if(response.data?.role) {
                    this.$store.state.role = response.data.role;
                }
            }
            catch (error) {
                this.error = true
            }
        },
        resetPasswordClicked(e) {
            e.preventDefault()
            this.reset_password = true
        },
        loginClicked(e) {
            e.preventDefault()
            this.reset_password = false
        },
        async resetPassword(e){
            e.preventDefault()
            try {
                this.sending = true
                const response = await noAuthAxiosInstance.post(`/auth/password_reset/`, {
                    email:this.username,
                });

                Swal.fire(
                    'Şifre Sıfırlama Maili Gönderildi!',
                    '',
                    'success'
                )
            }catch (e) {
                Swal.fire(
                    'Hata',
                    'Şifre Sıfırlama Maili Gönderilemedi!',
                    'error'
                )
            }
            this.sending = false
            this.reset_password = false
        }
    }
};
</script>
