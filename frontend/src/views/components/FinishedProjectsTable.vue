<template>
  <div class="card mb-4 finished-table" :style="mainStyle">
    <div class="card-header pb-0">
      <h6>Gerçekleşen Fırsatlar</h6>

    </div>
    <div class="card-body px-0 pt-0 pb-2">
      <div class="table-responsive p-0">
        <table class="table align-items-center justify-content-center mb-0">
          <thead>
            <tr>
              <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                Son Kullanıcı
              </th>
              <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                İş Ortağı
              </th>
                <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                    Account Manager
                </th>
              <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ">
                Fatura Tarihi
              </th>

              <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                Ürün
              </th>

              <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                Adet
              </th>

              <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                Bütçe
              </th>

              <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                Bitiş Tarihi
              </th>

              <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                Fatura Miktarı
              </th>

                <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                    Dosyalar
                </th>
                <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(project, i) in projects" :key="i">
              <td  class="align-middle ">
                <span class="ms-3 text-xs font-weight-bold">{{ projectDetails[i].client?.name }}</span>

              </td>
              <td class="align-middle ">
                <span class="text-xs font-weight-bold ms-3">{{ projectDetails[i].partner?.name }}</span>

              </td>
                <td class="align-middle ">
                    <span  class="text-xs font-weight-bold ms-3">{{ projectDetails[i].manager?.first_name }} {{ projectDetails[i].manager?.last_name }}</span>

                </td>
                <td class="align-middle ">
                    <span class="text-xs font-weight-bold ms-3">{{ project?.invoice_date }}</span>
                </td>

              <td class="align-middle ">
                <span class="text-xs font-weight-bold ms-3">{{ projectDetails[i].product?.name }}</span>
              </td>

              <td class="align-middle ">
                <span  class="text-xs font-weight-bold ms-3">{{ project?.count}}</span>

              </td>

              <td class="align-middle ">
                <span class="text-xs font-weight-bold ms-3">{{ project?.budget }}$</span>

              </td>

              <td class="align-middle ">
                <span  class="text-xs font-weight-bold ms-3">{{ project?.end_date }}</span>

              </td>

              <td class="align-middle ">
                <span class="text-xs font-weight-bold ms-3">{{ project?.invoice_amount }}</span>
              </td>

                <td class="align-middle ">
                    <Popper class="light">
                        <span class="text-xs font-weight-bold ms-3">Dosyaları Görüntüle</span>
                        <template #content>
                            <a v-for="file in projectDetails[i]?.projFiles " style="cursor: pointer" @click="download(file.id)" class="text-xs font-weight-bold">{{formatFile(file.file)}}<br></a>
                        </template>
                    </Popper>
                </td>
                <td>
                    <a @click="deleteProject($event ,project)" class="btn btn-link text-danger text-gradient px-3 mb-0" >
                        <i class="far fa-trash-alt me-2" aria-hidden="true"></i>
                    </a>
                </td>

<!--                <td class="align-middle text-center">-->
<!--                    <span class="text-xs font-weight-bold">-->
<!--                        <router-link :to="{ name: 'bill', params: { id: project.id} }" target="_blank"><i class="fa fa-external-link"></i></router-link>-->
<!--                    </span>-->
<!--                </td>-->
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
<style>
.popper{
    max-width: 300px;
    white-space: break-spaces;

}
.light {
    text-decoration: underline;
    cursor: pointer;
    --popper-theme-background-color: #ffffff;
    --popper-theme-background-color-hover: #ffffff;
    --popper-theme-text-color: #333333;
    --popper-theme-border-width: 1px;
    --popper-theme-border-style: solid;
    --popper-theme-border-color: #eeeeee;
    --popper-theme-border-radius: 6px;
    --popper-theme-padding: 32px;
    --popper-theme-box-shadow: 0 6px 30px -6px rgba(0, 0, 0, 0.25);
}

</style>
<script>
import axios from "axios";
import moment from "moment";
import VueSlider from "vue-slider-component";
import 'vue-slider-component/theme/default.css';
import VsudProgress from "@/components/VsudProgress.vue";
import {axiosInstance} from "@/utils/utils";
import Swal from "sweetalert2";

export default {
  name: "FinishedProjectsTable",
  components: {
      VsudProgress,
      VueSlider
  },
  data() {
    return {
      clients: [],
      partners: [],
      projects: [],
      people: [],
      users:[],
      products: [],
      client: "",
      partner: "",
      invoiceDate: "",
      product: "",
      endDate: "",
      count : "",
      budget: "",
      user:"",
      loading : true,
      files: null
    }
  },
  async created() {
    this.loading = true
    const clientsResp = await axiosInstance.get(`/kurumlar/rol/client`);
    if(clientsResp.data.data){
      this.clients = clientsResp.data.data;
    }
    const partnersRes = await axiosInstance.get(`/kurumlar/rol/partner`);
    if(partnersRes.data.data){
      this.partners = partnersRes.data.data;
    }

    const productRes = await axiosInstance.get(`/urunler`);
        this.products = productRes.data?.data;

    const projectsRes = await axiosInstance.get(`/sonlanan/`);
    if(projectsRes) {
        this.projects = projectsRes.data.data;
        this.formatObj(this.projects);
    }
    const peopleResp =  await axiosInstance.get(`/kisiler`);
    this.people = peopleResp.data.data

    const usersRes = await axiosInstance.get(`/auth/kullanicilar`);
    if(usersRes.data.data){
        this.users = usersRes.data.data;
    }

    const filesRes = await axiosInstance.get(`/dosyalar`);
    if(filesRes.data.data){
        this.files = filesRes.data.data;
    }
    this.loading = false
  },
  computed: {
      mainStyle() {
          return {
              opacity: this.loading ? 0 : 1
          }
      },
      projectDetails() {
        return this.projects.map(project => {
            const client = this.clients.find(c => c.id === project?.client);
            const partner = this.partners.find(c => c.id === project?.partner);
            const product = this.products.find(prod => prod.id === project?.product);
            const manager = this.users.find(user => user.id === project?.registered_by)
            let projFiles = null
            if(this.files !== null) {
                projFiles = this.files.filter(file => file?.project === project?.id || !project?.id)

            }
            return { client, partner, product, project,manager, projFiles };
        });
      }
  },
   methods: {

    formatDate(dateInput, format = 'DD.MM.YYYY') {
      return moment(dateInput).format(format)
    },

    async download(id) {
          let response = await axiosInstance.get(`/download/${id}`, {
              responseType:"blob",
          })
        let filename = "sozlesme.pdf"
        if (typeof response.headers["content-disposition"] === "string") {
            let regex = /filename="([^"]+)"/.exec((response.headers["content-disposition"]))
            if(regex) {
                filename = regex[1]
            }
        }

          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', filename);
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          window.URL.revokeObjectURL(url);
        },
     formatFile(file) {
         if (file.match(/\/sozlesmeler\/(.+)/)[1])
          return file.match(/\/sozlesmeler\/(.+)/)[1]
     },
    formatObj(projList) {
       if(Array.isArray(projList)){
           for (const project of projList) {
               if (project.end_date) {
                   project.end_date = this.formatDate(project.end_date)
               }
               if (project.invoice_date) {
                   project.invoice_date = this.formatDate(project.invoice_date)
               }
           }
       }
      else {
           if (projList.end_date) {
               projList.end_date = this.formatDate(projList.end_date)
           }
           if (projList.invoice_date) {
               projList.invoice_date = this.formatDate(projList.invoice_date)
           }
       }
    },
       deleteProject(e, project) {
           e.preventDefault()
           Swal.fire({
               title: 'Bu fırsatı silmek istediğinize emin misiniz?',
               text: "",
               icon: 'warning',
               showCancelButton: true,
               confirmButtonColor: '#3085d6',
               cancelButtonColor: '#d33',
               confirmButtonText: 'Sil',
               cancelButtonText:'İptal'
           }).then(async (result) => {
               if (result.isConfirmed) {
                   try {
                       await axiosInstance.delete(`/sonlanan/${project.id}`, {
                       });
                       await axiosInstance.delete(`/firsatlar/${project.project}/`, {
                       });
                       this.projects = this.projects.filter(proj => proj.id !== project.id);
                       Swal.fire(
                           'Fırsat Başarıyla Silindi',
                           '',
                           'success'
                       )
                   }
                   catch (e) {
                       Swal.fire(
                           'Hata',
                           'Fırsat Silinemedi!',
                           'error'
                       )
                   }
               }
           })
       }
  },
  watch: {
    client: {
      handler() {
        this.clientContact = null;
      },
      immediate: false
    },
    partner: {
        handler() {
            this.clientContact = null;
        },
        immediate: false
    },
  }
};
</script>

<style lang="scss">
.finished-table{
  transition: opacity linear 0.1s;
}
</style>
