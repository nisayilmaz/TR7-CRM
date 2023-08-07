<template>
    <div class="card mb-4 projects-table" :style="mainStyle">
        <div class="card-header pb-0">
            <h6>{{formatTitle(typeProp)}} Fırsatlar</h6>

        </div>
        <div class="card-body px-0 pt-0 pb-2">
            <div class="table table-striped table-responsive p-0 ">
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
                            Fırsat Tarihi
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
                            POC
                        </th>

                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                            Tahmini Kapanış Tarihi
                        </th>

                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                            İlgili Kişi
                        </th>

                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                            Proje Sorumlusu
                        </th>

                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                            İhale Tarihi
                        </th>

                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                            Olasılık
                        </th>

                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                            Açıklama
                        </th>

                        <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                            Detay
                        </th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-for="(project, i) in projects" :key="i">
                        <td  class="align-middle ">
                  <span v-if="projectDetails[i].client" class="text-xs font-weight-bold ms-3">
                    <router-link :to="{ name: 'CompanyDetail', params: { id: projectDetails[i].client.id}}" >{{ projectDetails[i].client?.name }}</router-link>
                    </span>
                            <span v-else class="text-xs font-weight-bold ms-3">
                      -
                    </span>

                        </td>
                        <td class="align-middle ">
                <span v-if="projectDetails[i].partner" class="text-xs font-weight-bold ms-3">
                    <router-link :to="{ name: 'CompanyDetail', params: { id: projectDetails[i].partner.id}}" >{{ projectDetails[i].partner?.name }}</router-link>
                    </span>
                            <span v-else class="text-xs font-weight-bold ms-3">
                      -
                    </span>
                        </td>
                        <td class="align-middle ">
                            <span  class="text-xs font-weight-bold ms-3">{{ projectDetails[i].user?.first_name }} {{ projectDetails[i].user?.last_name }}</span>

                        </td>
                        <td class="align-middle ">
                            <span class="text-xs font-weight-bold ms-3">{{ project?.registration_date }}</span>
                        </td>

                        <td class="align-middle ">
                            <span class="text-xs font-weight-bold ms-3">{{ projectDetails[i].product?.name }}</span>
                        </td>

                        <td class="align-middle ">
                            <span class="text-xs font-weight-bold ms-3">{{ project?.count}}</span>

                        </td>

                        <td class="align-middle ">
                            <span class="text-xs font-weight-bold ms-3">{{ project?.budget }}$</span>

                        </td>

                        <td class="align-middle ">
                            <span class="text-xs font-weight-bold ms-3">{{ project?.poc_request }}</span>

                        </td>

                        <td class="align-middle ">
                            <span class="text-xs font-weight-bold ms-3">{{ project?.exp_end_date }}</span>
                        </td>

                        <td class="align-middle ">
                            <span class="text-xs font-weight-bold ms-3">{{projectDetails[i].client_contact?.first_name}} {{ projectDetails[i].client_contact?.last_name}}</span>
                        </td>

                        <td class="align-middle ">
                            <span class="text-xs font-weight-bold ms-3">{{projectDetails[i].partner_contact?.first_name}} {{ projectDetails[i].partner_contact?.last_name}}</span>
                        </td>

                        <td class="align-middle ">
                            <span class="text-xs font-weight-bold ms-3">{{ project?.tender_date }}</span>
                        </td>

                        <td class="align-middle ">
                <span class="text-xs font-weight-bold ms-3">
                    <Popper :hover="true">
                      <vsud-progress
                              :percentage="project?.probability"
                      />
                      <template #content>
                        <div>%{{ project?.probability }}</div>
                      </template>
                    </Popper>
                   </span>

                        </td>

                        <td class="align-middle ">
                <span class="text-xs font-weight-bold ms-3">
                    <Popper :hover="true">
                      <i class="far fa-question-circle"></i>
                      <template #content>
                        <div>{{ project?.info }}</div>
                      </template>
                    </Popper>
                    </span>
                        </td>
                        <td class="align-middle ">
                    <span class="text-xs font-weight-bold ms-3">
                        <router-link :to="{ name: 'ProjectDetail', params: { id: project.id} }">  <i class="fa fa-external-link"></i></router-link>
                    </span>
                        </td>
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
:root {
    --popper-theme-background-color: #333333;
    --popper-theme-background-color-hover: #333333;
    --popper-theme-text-color: #ffffff;
    --popper-theme-border-width: 0px;
    --popper-theme-border-style: solid;
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
import {th} from "vuetify/locale";
import Swal from "sweetalert2";
import projects from "@/views/Projects.vue";
import {axiosInstance} from "@/utils/utils";
export default {
    name: "ClosedProjectsTable",
    components: {
        VsudProgress,
        VueSlider
    },
    props: {
        filter : {
            type: String,
            default : 0
        },
        typeProp : {
            type: String
        }
    },
    data() {
        return {
            clients: [],
            partners: [],
            projects: [],
            people: [],
            users:[],
            clientEmp: [],
            partnerEmp: [],
            products: [],
            client: null,
            partner: null,
            startDate: null,
            product: null,
            poc: null,
            endDate: null,
            clientContact: null,
            partnerContact: null,
            tenderDate: null,
            explanation: null,
            probability: 0,
            count : null,
            budget: null,
            probValues : [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100],
            user:null,
            loading:true,
            response : true
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

        const projectsRes = await axiosInstance.get(`/firsatlar`);
        if(projectsRes) {
            this.projects = projectsRes.data.data;
            this.formatObj(this.projects);
            this.projects = this.projects.filter(project => project.poc_request === this.typeProp );
            if (this.filter !== "0") {
                this.projects = this.projects.filter(project => project.client === parseInt(this.filter) || project.partner === parseInt(this.filter))
            }

        }
        const peopleResp =  await axiosInstance.get(`/kisiler`);
        this.people = peopleResp.data.data

        const usersRes = await axiosInstance.get(`/auth/kullanicilar`);
        if(usersRes.data.data){
            this.users = usersRes.data.data;
        }
        this.loading = false

    },
    computed: {
        mainStyle() {
            return {
                opacity: this.loading ? 0 : 1
            }
        },
        clientEmployees() {
            if (!Array.isArray(this.people)) return []
            return this.people.filter(person => person.company === this.client)
        },
        partnerEmployees() {
            if (!Array.isArray(this.people)) return []
            return this.people.filter(person => person.company === this.partner)
        },
        projectDetails() {
            return this.projects.map(project => {
                const client = this.clients.find(c => c.id === project?.client);
                const partner = this.partners.find(c => c.id === project?.partner);
                const client_contact = this.people.find(person => person.id === project?.client_contact);
                const partner_contact = this.people.find(person => person.id === project?.partner_contact);
                const product = this.products.find(prod => prod.id === project?.product);
                const user = this.users.find(usr => usr.id === project?.registered_by);
                return { client, partner, client_contact, partner_contact, product, project, user };
            });
        }
    },
    methods: {
        formatDate(dateInput, format = 'DD.MM.YYYY') {
            return moment(dateInput).format(format)
        },

        formatPoc(poc) {
            let options = { 1: "Toplantı Aşaması", 2: "POC Talebi",3: "POC Aşaması", 4: "POC Gerçekleştirildi",5: "Yaklaşık Maliyet", 6: "Alım Aşaması",7: "Pazarlık Aşaması", 8: "Gerçekleşti", 9:"Kapandı", 10:"Kaybedildi" }
            poc = options[poc]
            return poc
        },
        formatTitle(title) {
            let options = { "Kapandı" : "Kapanan", "Kaybedildi": "Kaybedilen" }
            title = options[title]
            return title
        },
        formatObj(projList) {
            if(Array.isArray(projList)){
                for (const project of projList) {
                    if (project.registration_date) {
                        project.registration_date = this.formatDate(project.registration_date)
                    }
                    if (project.exp_end_date) {
                        project.exp_end_date = this.formatDate(project.exp_end_date)
                    }
                    if (project.tender_date) {
                        project.tender_date = this.formatDate(project.tender_date)
                    }
                    project.poc_request = this.formatPoc(project.poc_request)
                }
            }
            else {
                if (projList.exp_end_date) {
                    projList.registration_date = this.formatDate(projList.registration_date)
                }
                if (projList.exp_end_date) {
                    projList.exp_end_date = this.formatDate(projList.exp_end_date)
                }
                if (projList.tender_date) {
                    projList.tender_date = this.formatDate(projList.tender_date)
                }
                projList.poc_request = this.formatPoc(projList.poc_request)
            }
        },
    },

};
</script>

<style lang="scss">
.projects-table{
  transition: opacity linear 0.07s;
}
</style>