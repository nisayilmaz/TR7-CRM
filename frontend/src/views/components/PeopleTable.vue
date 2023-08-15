<template>
    <div class="card mb-4 people-table" :style="mainStyle">
      <div class="card-header pb-0">
        <h6>Kişiler</h6>
        <div v-if="company_filter === '0'" class="accordion accordion-flush" id="accordionFlushExample">
          <div class="accordion-item">
            <div class="d-flex justify-content-between accordion-header">
              <button class=" ps-0 accordion-button collapsed " type="button" data-bs-toggle="collapse" data-bs-target="#addPeople" aria-expanded="false" aria-controls="flush-collapseOne">
                  Kişi Ekle <i class="fa fa-plus ms-2" aria-hidden="true"></i>
              </button>
                <vsud-button  @click="downloadSummary">Özet İNDİR</vsud-button>

            </div>

              <div id="addPeople" class="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
              <div class="accordion-body row">
                <div class="col-6">
                    <div class="mb-3">
                        <label for="name" class="form-label">Ad*</label>
                        <input v-model="first_name" type="text" class="ps-0 form-control" id="firstName">
                    </div>

                    <div class="mb-3">
                        <label for="surname" class="form-label">Soyad*</label>
                        <input v-model="last_name" type="text" class="ps-0 form-control" id="lastName">
                    </div>

                    <div class="mb-3">
                        <label for="email" class="form-label">Email</label>
                        <input v-model="email" type="text" class="ps-0 form-control" id="email">
                    </div>
                    <button type="submit" class="btn btn-primary pull-right" v-if="response" @click="addPerson">Ekle</button>
                    <div v-if="!response" class="spinner-border ms-2" role="status">
                        <span class="sr-only">Loading...</span>
                    </div>
                </div>
                <div class="col-6">
                    <div class="mb-3">
                        <label for="phone" class="form-label">Telefon</label>
                        <input v-model="phone" type="text" class="ps-0 form-control" id="phone">
                    </div>

                    <div class="mb-4">
                        <label for="company" class="form-label">Kurum/İş Ortağı*</label>
                        <select id="client" v-model="company" class="form-select"  >
                            <option value="null" selected>Kurum/İş Ortağı Seçin</option>
                            <option v-for="company in companies" :key="company.id" :value="company.id">{{company.name}}</option>
                        </select>
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
                  <SearchInput v-if="company_filter === '0'" type="search"
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
                <th
                  class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                  Ad
                </th>
                <th
                  class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">
                  Soyad
                </th>
                <th
                  class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">
                  Email
                </th>
                <th
                  class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">
                  Telefon
                </th>
                <th
                  class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">
                    Kurum/İş Ortağı
                </th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="person in filteredData" :key="person.id">
                <td>
                  <div class="d-flex px-2">
                    <div class="my-auto">
                      <h6 class="mb-0 text-sm">{{person.first_name}}</h6>
                    </div>
                  </div>
                </td>
                <td>
                  <p class="text-sm font-weight-bold mb-0">{{person.last_name}}</p>
                </td>
                <td>
                  <span class="text-xs font-weight-bold">{{person.email}}</span>
                </td>
                <td >
                    <span class="me-2 text-xs font-weight-bold">{{person.phone}}</span>
                </td>
                <td class="align-middle">
                    <span class="me-2 text-xs font-weight-bold">{{ getCompanyName(person.company) }}</span>

                </td>
                <td class="align-middle">

                    <a class="me-4 text-secondary font-weight-bold text-xs" @click="deletePerson($event, person.id)">
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
  import Swal from "sweetalert2";
  import {axiosInstance} from "@/utils/utils";
  import SearchInput from 'vue-search-input'
  import 'vue-search-input/dist/styles.css'
  import VsudButton from "@/components/VsudButton.vue";


  export default {
    name: "PeopleTable",
    props: {
      company_filter :{
          type:String,
          default:0
      }
    },
    components: {
        VsudButton,
        SearchInput
    },
    data() {
      return {
        companies : [],
        people : [],
        first_name : "",
        last_name : "",
        email : "",
        phone: "",
        company: null,
        search: "",
        loading : true,
        filter: parseInt(this.company_filter),
        response: true
      }
    },
    async created() {
        this.loading = true
        const companiesRes = await axiosInstance.get(`/kurumlar/`);
        if (companiesRes.data.status === "success") {
            this.companies = companiesRes.data.data;
        }
        const people = await axiosInstance.get(`/kisiler/`);
        this.people = people.data.data;
        if(this.company_filter !== '0') {
            this.people = this.people.filter(person => person.company === parseInt(this.company_filter))
        }
        this.loading = false
    },
      computed: {
        mainStyle() {
            return {
                opacity: this.loading ? 0 : 1
            }
        },
        filteredData() {
            return this.people.filter(person => {
                return (person?.first_name + person?.last_name + this.getCompanyName(person?.company)).toString().toLowerCase().includes(this.search.toLowerCase())})
        }
      },
    methods: {
      async addPerson(e) {
        e.preventDefault();
        this.response = false
        try {
            const response = await axiosInstance.post(`/kisiler/`, {
                    first_name : this.first_name,
                    last_name : this.last_name,
                    phone : this.phone,
                    email : this.email,
                    company : this.company
                });
            let lastId =  response.data.data.id;
            const personRes = await axiosInstance.get(`/kisiler/${lastId}`);

            const addPerson = personRes.data.data
            const index = this.people.findIndex(person => addPerson.first_name.localeCompare(person.first_name) < 0);
            const insertIndex = index === -1 ? this.people.length : index;
            this.people.splice(insertIndex, 0, addPerson);

            Swal.fire(
                'Kişi Başarıyla Eklendi',
                '',
                'success'
            )
            this.response = true
        }
        catch (err) {
            Swal.fire(
                'Hata',
                'Kişi Eklenemedi!',
                'error'
            )
            this.response = true
        }
        this.first_name = "";
        this.last_name = "";
        this.email = "";
        this.phone = "";
        this.company = "";
      },
      async deletePerson(e, id) {
          e.preventDefault();
          Swal.fire({
              title: 'Bu kişiyi silmek istediğinize emin misiniz?',
              text: "Bu işlem geri alınamaz ve kişiyle ilişkili tüm fırsatlar da silinir.",
              icon: 'warning',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: 'Sil',
              cancelButtonText:'İptal'
          }).then(async (result) => {
              if (result.isConfirmed) {
                  await axiosInstance.delete(`/kisiler/${id}`);
                  this.people = this.people.filter(person => person.id !== id);
              }
          })

      },
      getCompanyName(companyId) {
          if(!Array.isArray(this.companies)) return " "
          const comp = this.companies.find(c => c.id === companyId);
          return comp ? comp.name : " ";
      },
      async downloadSummary() {
          try{
              const response = await axiosInstance.get("/excel/4",{
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
.people-table{
  transition: opacity linear 0.1s;
}
</style>