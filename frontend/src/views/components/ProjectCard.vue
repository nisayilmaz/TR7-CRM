<template>
    <div class="card h-100">
        <div class="p-3 pb-0 card-header">
            <div class="row">
                <div class="col-md-8 d-flex align-items-center">
                    <h6 class="mb-0">Fırsat Detayı</h6>
                </div>
                <div class="col-md-4 text-end">
                    <a class="btn btn-link text-danger text-gradient px-3 mb-0" href="javascript:;">
                        <i @click="this.deleteProject($event,project.id)"
                            class="far fa-trash-alt me-2" aria-hidden="true"></i>
                    </a>
                    <a v-if="!edit" href="javascript:;">
                        <i @click="this.clickEdit"
                           class="text-sm fa fa-pencil-square-o text-secondary"
                        ></i>
                    </a>
                    <a v-if="edit" href="javascript:;">
                        <i @click="this.cancelEdit"
                           class="text-sm fa fa-ban text-secondary"
                        ></i>
                    </a>
                </div>
            </div>
        </div>
        <div v-if="!edit" class="p-3 card-body">
            <p class="text-sm">
                <strong class="text-dark">Açıklama:</strong>&nbsp;{{ project?.info }}
            </p>
            <ul class="list-group">
                <li class="pt-0 text-sm border-0 list-group-item ps-0">
                    <strong class="text-dark">Son Kullanıcı:</strong>&nbsp;{{ projectDetails.client?.name }}
                </li>
                <li class="text-sm border-0 list-group-item ps-0">
                    <strong class="text-dark">İş Ortağı:</strong>&nbsp;{{ projectDetails.partner?.name }}
                </li>
                <li class="text-sm border-0 list-group-item ps-0">
                    <strong class="text-dark">Account Manager:</strong>&nbsp;{{ projectDetails.user?.first_name }}
                    {{ projectDetails.user?.last_name }}
                </li>
                <li class="text-sm border-0 list-group-item ps-0">
                    <strong class="text-dark">Fırsat Eklenme
                        Tarihi:</strong>&nbsp;{{ formatDate(project?.registration_date) }}
                </li>
                <li class="text-sm border-0 list-group-item ps-0">
                    <strong class="text-dark">İhale Tarihi:</strong>&nbsp;{{ formatDate(project?.tender_date) }}
                </li>
                <li class="text-sm border-0 list-group-item ps-0">
                    <strong class="text-dark">Tahmini Kapanış
                        Tarihi:</strong>&nbsp;{{ formatDate(project?.exp_end_date) }}
                </li>
                <li class="text-sm border-0 list-group-item ps-0">
                    <strong class="text-dark">Son Kullanıcı İlgili
                        Kişi:</strong>&nbsp;{{ projectDetails.client_contact?.first_name }}
                    {{ projectDetails.client_contact?.last_name }}
                </li>
                <li class="text-sm border-0 list-group-item ps-0">
                    <strong class="text-dark">İş Ortağı İlgili
                        Kişi:</strong>&nbsp;{{ projectDetails.partner_contact?.first_name }}
                    {{ projectDetails.partner_contact?.last_name }}
                </li>
                <li class="text-sm border-0 list-group-item ps-0">
                    <strong class="text-dark">Ürün:</strong>&nbsp;{{ projectDetails.product?.name }}
                </li>
                <li class="text-sm border-0 list-group-item ps-0">
                    <strong class="text-dark">Adet:</strong>&nbsp;{{ project?.count }}
                </li>
                <li class="text-sm border-0 list-group-item ps-0">
                    <strong class="text-dark">Bütçe:</strong>&nbsp;{{ project?.budget }}$
                </li>
                <li class="text-sm border-0 list-group-item ps-0">
                    <strong class="text-dark">POC :</strong>&nbsp;{{ formatPoc(project?.poc_request) }}
                </li>
                <li class="text-sm border-0 list-group-item ps-0">
                    <strong class="text-dark">Olasılık:</strong>&nbsp;{{ project?.probability }}%
                </li>
            </ul>
        </div>
        <div v-if="edit" class="p-3 card-body">
            <form class="row" enctype="multipart/form-data">
                <div class="col-4">
                    <div class="mb-3">
                        <label for="client" class="form-label">Son Kullanıcı</label>
                        <select v-model="client" class="form-select" id="client" @change="dropdownListener">
                            <option selected>Kurum Seçin</option>
                            <option v-for="client in clients" :id="client.id" :value="client.id">{{ client.name }}</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="partner" class="form-label">İş Ortağı</label>
                        <select v-model="partner" class="form-select" id="partner" @change="dropdownListener">
                            <option value="null" selected>Kurum Seçin</option>
                            <option v-for="partner in partners" :id="partner.id" :value="partner.id">{{ partner.name }}</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="accountmngr" class="form-label">Account Manager</label>
                        <select v-model="user" class="form-select" id="partner" @change="dropdownListener">
                            <option selected>Kurum Seçin</option>
                            <option v-for="user in users" :id="user.id" :value="user.id">{{ user.first_name }} {{ user.last_name }}</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="startDate" class="form-label">Fırsat Tarihi</label>
                        <input v-model="startDate" type="date" class="ps-0 form-control" id="startDate">
                    </div>
                    <div class="mb-3">
                        <label for="product" class="form-label">Ürün</label>
                        <select v-model="product" class="form-select" id="product">
                            <option selected>Ürün Seçin</option>
                            <option v-for="product in products" :key="product.id" :value="product.id"> {{product.name}} </option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="count" class="form-label">Adet</label>
                        <input v-model="count"  type="text" class="ps-0 form-control" id="count">
                    </div>
                </div>
                <div class="col-4">
                    <div class="mb-3">
                        <label for="client_contact" class="form-label">İlgili Kişi</label>
                        <select v-model="clientContact" class="form-select" id="client_contact">
                            <option selected></option>
                            <option v-for="emp in clientEmployees" :id="emp.id" :value="emp.id"> {{ emp.first_name }} {{ emp.last_name }}
                            </option>
                        </select>
                    </div>

                    <div class="mb-3">
                        <label for="partner_contact" class="form-label">Proje Sorumlusu</label>
                        <select v-model="partnerContact" class="form-select" id="partner_contact">
                            <option selected></option>
                            <option v-for="emp in partnerEmployees" :id="emp.id" :value="emp.id"> {{ emp.first_name }} {{ emp.last_name}}
                            </option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="poc" class="form-label">POC</label>
                        <select v-model="poc" class="form-select" id="poc">
                            <option selected></option>
                            <option value="1"> Toplantı Aşaması </option>
                            <option value="2"> POC Talebi </option>
                            <option value="3"> POC Aşaması </option>
                            <option value="4"> POC Gerçekleştirildi </option>
                            <option value="5"> Yaklaşık Maliyet </option>
                            <option value="6"> Alım Aşaması </option>
                            <option value="7"> Pazarlık Aşaması </option>
                            <option value="8"> Gerçekleşti </option>
                            <option value="9"> Kapandı </option>
                            <option value="10"> Kaybedildi </option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="endDate" class="form-label">Tahmini Kapanış Tarihi</label>
                        <input v-model="endDate" type="date" class="ps-0 form-control" id="endDate">
                    </div>
                    <div class="mb-3">
                        <label for="probability" class="form-label">Olasılık</label>
                        <vue-slider id="probability"
                                    v-model="probability"
                                    :data="probValues"
                                    :marks="false"
                        ></vue-slider>
                    </div>
                </div>
                <div class="col-4">
                    <div class="mb-3">
                        <label for="tenderDate" class="form-label">İhale Tarihi</label>
                        <input v-model="tenderDate" type="date" class="ps-0 form-control" id="tenderDate">
                    </div>
                    <div class="mb-3">
                        <label for="budget" class="form-label">Bütçe</label>
                        <input v-model="budget" type="text" class="ps-0 form-control" id="budget">
                    </div>
                    <div class="mb-3">
                        <label for="explanation" class="form-label">Açıklama</label>
                        <input v-model="explanation" type="text" class="ps-0 form-control" id="explanation">
                    </div>
                    <div v-if="poc === '8' || poc === 8" class="mb-3">
                        <label for="file" class="form-label">Dosyalar</label>
                        <input type="file" class="ps-0 form-control" @change="handleFile" id="file" multiple>
                    </div>

                    <div v-if="poc === '8' || poc === 8" class="mb-3">
                        <label for="finDate" class="form-label">Bitiş Tarihi*</label>
                        <input v-model="finDate" type="date" class="ps-0 form-control"  id="finDate">
                    </div>

                    <div v-if="poc === '8' || poc === 8" class="mb-3">
                        <label for="invoiceDate" class="form-label">Fatura Tarihi*</label>
                        <input  v-model="invoiceDate" type="date" class="ps-0 form-control" id="invoiceDate">
                    </div>

                    <div v-if="poc === '8' || poc === 8" class="mb-3">
                        <label for="invoiceAmount" class="form-label">Fatura Miktarı*</label>
                        <input  v-model="invoiceAmount" type="text" class="ps-0 form-control" id="invoiceAmount">
                    </div>
                </div>

            </form>
            <button @click="updateProject($event,project.id)" type="submit" class="btn btn-primary">Güncelle</button>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import users from "@/views/Users.vue";
import moment from "moment/moment";
import VueSlider from "vue-slider-component";
import 'vue-slider-component/theme/default.css';
import Swal from 'sweetalert2'
import {axiosInstance} from "@/utils/utils";

export default {
    name: "ProjectCard",
    components: {
        VueSlider
    },
    props: {
        project: {
            type: Object,
            default: null
        }
    },
    data() {
        return {
            clients: [],
            partners: [],
            products: [],
            people: [],
            users: [],
            client: null,
            partner: null,
            startDate: "",
            product: null,
            poc: "",
            endDate: "",
            clientContact: null,
            partnerContact: null,
            tenderDate: "",
            explanation: "",
            probability: 0,
            count: "",
            budget: "",
            probValues: [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100],
            user: "",
            edit: false,
            note: "",
            title: "",
            files: null,
            finDate: "",
            invoiceDate: "",
            invoiceAmount: ""
        }
    },
    async created() {
        const clientsResp = await axiosInstance.get(`/kurumlar/rol/client`);
        if (clientsResp.data.data) {
            this.clients = clientsResp.data.data;
        }
        const partnersRes = await axiosInstance.get(`/kurumlar/rol/partner`);
        if (partnersRes.data.data) {
            this.partners = partnersRes.data.data;
        }

        const productRes = await axiosInstance.get(`/urunler`);
        this.products = productRes.data?.data;

        const peopleResp = await axiosInstance.get(`/kisiler`);
        this.people = peopleResp.data.data

        const usersRes = await axiosInstance.get(`/auth/kullanicilar`);
        if (usersRes.data.data) {
            this.users = usersRes.data.data;
        }
    },
    computed: {
        projectDetails() {
            const client = this.clients.find(c => c.id === this.project?.client);
            const partner = this.partners.find(c => c.id === this.project?.partner);
            const client_contact = this.people.find(person => person.id === this.project?.client_contact);
            const partner_contact = this.people.find(person => person.id === this.project?.partner_contact);
            const product = this.products.find(prod => prod.id === this.project?.product);
            const user = this.users.find(usr => usr.id === this.project?.registered_by);
            return {client, partner, client_contact, partner_contact, product, user};
        },

        clientEmployees() {
          if (!Array.isArray(this.people)) return []
          return this.people.filter(person => person.company === this.client)
        },
        partnerEmployees() {
          if (!Array.isArray(this.people)) return []
          return this.people.filter(person => person.company === this.partner)
        },
    },
    methods: {
        formatDate(dateInput, format = 'DD.MM.YYYY') {
            if(dateInput === null) {
                return null
            }
            return moment(dateInput).format(format)
        },
        formatPoc(poc) {
            let options = {
                1: "Toplantı Aşaması",
                2: "POC Talebi",
                3: "POC Aşaması",
                4: "POC Gerçekleştirildi",
                5: "Yaklaşık Maliyet",
                6: "Alım Aşaması",
                7: "Pazarlık Aşaması",
                8: "Gerçekleşti",
                9: "Kapandı",
                10: "Kaybedildi"
            }
            return options[poc]
        },
        clickEdit() {
            this.edit = true
            this.client = this.project?.client
            this.partner = this.project?.partner
            this.tenderDate = this.project?.tender_date
            this.startDate = this.project?.registration_date
            this.product = this.project?.product
            this.poc = this.project?.poc_request
            this.endDate = this.project?.exp_end_date
            this.explanation = this.project?.info
            this.probability =  this.project?.probability
            this.clientContact =  this.project?.client_contact
            this.partnerContact = this.project?.partner_contact
            this.count = this.project?.count
            this.budget = this.project?.budget
            this.user = this.project?.registered_by
        },
        cancelEdit() {
            this.edit = false
            this.client = ""
            this.partner = null
            this.tenderDate = ""
            this.startDate = ""
            this.product = null
            this.poc = ""
            this.endDate = ""
            this.explanation = ""
            this.probability =  ""
            this.clientContact =  null
            this.partnerContact = null
            this.count = ""
            this.budget = ""
            this.user = ""
        },
        handleFile(event) {
            this.files = event.target.files;
        },
        async deleteProject(e,id) {
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
                    await axiosInstance.delete(`/firsatlar/${id}/`, {
                    });
                    this.companies = this.companies.filter(company => company.id !== id);

                }
            })

        },
        async updateProject(e,id) {
            e.preventDefault()
            try {
                if (this.poc === 8 || this.poc === "8") {
                    const formData = new FormData();
                    if (this.files.length > 0) {
                        for (let i = 0; i < this.files.length; i++) {
                            formData.append('files', this.files[i]);
                        }
                    }else {
                        formData.append('files', "");

                    }
                    formData.append('client', this.client);
                    if (this.partner === null) {
                        formData.append('partner', "");

                    }else {
                        formData.append('partner', this.partner);
                    }
                    formData.append('count', this.count);
                    formData.append('budget', this.budget);
                    formData.append('invoice_date', this.invoiceDate);
                    formData.append('invoice_amount', this.invoiceAmount);
                    formData.append('product', 1);
                    formData.append('end_date', this.finDate);
                    formData.append('project', this.project.id);
                    formData.append('registered_by', this.user);
                    let resp = await axiosInstance.post(`/sonlanan/`, formData)
                }
                const response = await axiosInstance.put(`/firsatlar/${id}/`, {
                    client: this.client,
                    partner: this.partner,
                    registration_date: this.startDate,
                    product: this.product,
                    poc_request: this.poc,
                    exp_end_date:  this.endDate,
                    client_contact: this.clientContact,
                    partner_contact: this.partnerContact,
                    tender_date: this.tenderDate,
                    info: this.explanation,
                    probability: this.probability,
                    count: this.count,
                    budget: this.budget,
                    registered_by: this.user
                });
                const updated = await axiosInstance.get(`/firsatlar/${id}/`)
                this.$emit('updatedProj', updated.data.data)
                Swal.fire(
                    'Güncellendi',
                    'Fırsat Başarıyla Güncellendi!',
                    'success'
                )
            }catch (err) {
                Swal.fire(
                    'Hata',
                    'Fırsat Güncellenemedi!',
                    'error'
                )
            }
            this.edit = false
        }
    },

};
</script>
