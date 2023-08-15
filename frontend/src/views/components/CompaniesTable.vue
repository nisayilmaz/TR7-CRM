<template>
  <div class="card mb-4 companies-table" :style="mainStyle">
    <div class="card-header pb-0">
      <h6>{{title}}</h6>
      <div class="accordion accordion-flush" id="accordionFlushExample">
        <div class="accordion-item">
          <div class="d-flex justify-content-between accordion-header">
            <button class="ps-0 accordion-button collapsed " type="button" data-bs-toggle="collapse"
              data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">
              {{typeName}} Ekle <i class="fa fa-plus ms-2" aria-hidden="true"></i>
            </button>
              <vsud-button @click="downloadSummary" >Özet İNDİR</vsud-button>

          </div>

          <div id="flush-collapseOne" class="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
            <div class="accordion-body row">
              <div class="col-6">
                  <div class="mb-3">
                      <label for="name" class="form-label">İsim*</label>
                      <input v-model="name" type="text" class="ps-0 form-control" id="name">
                  </div>
                  <div class="mb-3">
                      <label for="phone" class="form-label">Telefon</label>
                      <input v-model="phone" type="text" class="ps-0 form-control" id="phone">
                  </div>
                  <button @click="addCompany" v-if="response" type="submit" class="btn btn-primary">Ekle</button>
                  <div v-if="!response" class="spinner-border ms-2" role="status">
                      <span class="sr-only">Loading...</span>
                  </div>
              </div>
              <div class="col-6">
                <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input v-model="email" type="text" class="ps-0 form-control" id="email">
                </div>
                <div class="mb-3">
                    <label for="address" class="form-label">Adres</label>
                    <input v-model="address" type="text" class="ps-0 form-control" id="address">
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="card-body px-0 pt-0 pb-2">
        <div class="row">
            <div class="col-3 ms-3">
                <SearchInput type="search"
                             v-model:modelValue="search"
                             wrapperClass="search-input-wrapper"
                             :searchIcon="true"
                             :shortcutIcon="true"
                             :clearIcon="true"
                />
            </div>

        </div>
      <div class="table-responsive p-0">
        <table class="table align-items-center justify-content-center mb-0">
          <thead>
            <tr>
              <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Kurum</th>
              <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Email</th>
              <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Telefon</th>
              <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Adres</th>
              <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">Account Manager</th>
              <th class="text-secondary opacity-7"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="element in data" :key="element.id">
              <td>
                <div class="d-flex px-2 py-1">
                  <div class="d-flex flex-column justify-content-center">
                    <h6 class="mb-0 text-sm">
                        <router-link :to="{ name: 'CompanyDetail', params: { id: element.company.id}}">{{ element.company.name }}</router-link></h6>
                    <!-- <p class="text-xs text-secondary mb-0">{{company.email}}</p> -->
                  </div>
                </div>
              </td>
              <td>
                <p class="text-xs font-weight-bold mb-0">{{ element.company.email }}</p>
              </td>
              <td class="align-middle text-sm">
                <p class="text-xs font-weight-bold mb-0">{{ element.company.phone }}</p>
              </td>
              <td class="align-middle text-sm">
                <p class="text-xs font-weight-bold mb-0">{{ element.company.address }}</p>
              </td>
                <td class="align-middle text-sm">
                <p  class="text-xs font-weight-bold mb-0">{{ element.registeredBy?.first_name }} {{ element.registeredBy?.last_name }}</p>
              </td>
              <td class="align-middle">
<!--                <a class="me-4 text-secondary font-weight-bold text-xs" >-->
<!--                  <i class="far fa-edit"></i>-->
<!--                </a>-->

                <a href="javascript:;" class="me-4 text-secondary font-weight-bold text-xs" @click="deleteCompany($event, element.company.id)">
                  <i class="far fa-trash-alt me-2"></i>
                </a>
              </td>
            </tr>

          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";
import {axiosInstance} from "@/utils/utils";
import SearchInput from 'vue-search-input'
import 'vue-search-input/dist/styles.css'
import VsudButton from "@/components/VsudButton.vue";
export default {

  name: "CompaniesTable",
  components: {
      VsudButton,
      SearchInput
  },
  props: {
      type: String,
  },
  data() {
      return {
          companies: [],
          users : [],
          name: "",
          phone: "",
          email: "",
          address: "",
          loading: true,
          response : true,
          search: ""
      };
  },
  computed: {
      data() {
          const filteredCompanies = this.companies.filter(company => {
              return (
                  (company?.name + company?.email + company?.phone + company?.address)
                      .toString()
                      .toLowerCase()
                      .includes(this.search.toLowerCase())
              );
          });

          const companyDetails = filteredCompanies.map(company => {
              const registeredBy = this.users.find(user => user.id === company?.registered_by_id);
              return { company,registeredBy };
          });

          return companyDetails;
      },
      mainStyle(){
        return {
            opacity: this.loading ? 0 : 1
        }
      },
      title() {
          if(this.type === 'client') {
              return 'Kurumlar'
          }
          else if(this.type === 'partner') {
              return 'İş Ortakları'
          }
      },
      typeName() {
          if(this.type === 'client') {
              return 'Kurum'
          }
          else if(this.type === 'partner') {
              return 'İş Ortağı'
          }
      },
  },
  async created() {
      try {
          this.loading = true
          const response = await axiosInstance.get(`/kurumlar/rol/${this.type}`)
          if (response.status === 200) {
              if (!Array.isArray(response.data.data)){
                  this.companies = []
              }
              else {
                  this.companies = response.data.data;
              }
          }
          const usersRes = await axiosInstance.get(`/auth/kullanicilar`);
          if(usersRes.data.data){
              this.users = usersRes.data.data;
          }
      }
      catch (err) {
      }
      this.loading = false

  },
  methods: {
    async addCompany(e) {
      e.preventDefault();
      try {
          this.response = false
          const response = await axiosInstance.post(`/kurumlar/`, {
              name: this.name,
              role: this.type,
              email: this.email,
              address: this.address,
              phone: this.phone,
          });
          const companyToAdd = response.data.data
          const index = this.companies.findIndex(company => companyToAdd.name.localeCompare(company.name) < 0);
          const insertIndex = index === -1 ? this.companies.length : index;
          this.companies.splice(insertIndex, 0, companyToAdd);

          Swal.fire(
              'Kurum/İş Ortağı Başarıyla Eklendi',
              '',
              'success'
          )
          this.response = true
          this.name = ""
          this.phone = ""
          this.email= ""
          this.address= ""
      }
      catch (error) {
          this.response = true
          Swal.fire(
              'Hata',
              'Kurum Eklenemedi!',
              'error'
          )
      }
    },
    async deleteCompany(e, id) {
      e.preventDefault();
        Swal.fire({
            title: 'Bu kurumu silmek istediğinize emin misiniz?',
            text: "Bu işlem geri alınamaz ve kurumla ilişkili tüm fırsatlar da silinir.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sil',
            cancelButtonText:'İptal'
        }).then(async (result) => {
            if (result.isConfirmed) {
                await axiosInstance.delete(`/kurumlar/${id}`, {
                   });
                this.companies = this.companies.filter(company => company.id !== id);

            }
        })
    },
      async downloadSummary() {
          try{
              let downloadType
              if (this.type === 'client'){
                  downloadType = 2
              }
              else if (this.type === 'partner'){
                  downloadType = 3
              }
              const response = await axiosInstance.get(`/excel/${downloadType}`,{
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
      }
  }
};
</script>

<style lang="scss">
  .companies-table{
    transition: opacity linear 0.1s;
  }
</style>