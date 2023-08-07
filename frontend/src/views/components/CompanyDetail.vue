<template>
    <div class="py-4 container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="card mb-4">
                    <div v-if="this.exists" class="card h-100">
                        <div class="p-3 pb-0 card-header">
                            <div class="row">
                                <div class="col-md-8 d-flex align-items-center">
                                    <h6 class="mb-0">Kurum Detayı</h6>
                                </div>
                                <div class="col-md-4 text-end">
                                    <a class="btn btn-link text-danger text-gradient px-3 mb-0" href="javascript:;">
                                        <i @click="this.deleteCompany($event,company.id)"
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
                                <strong class="text-dark">Kurum Adı:</strong>&nbsp;
                                <span> {{ company?.name }} </span>
                            </p>
                            <ul class="list-group">
                                <li class="pt-0 text-sm border-0 list-group-item ps-0">
                                    <strong class="text-dark">Adres:</strong>&nbsp;
                                    <span v-if="company?.address !== '' ">{{ company?.address }}</span>
                                    <span v-else>-</span>
                                </li>
                                <li class="text-sm border-0 list-group-item ps-0">
                                    <strong class="text-dark">Telefon:</strong>&nbsp;
                                    <span v-if="company?.phone !== '' ">{{ company?.phone }}</span>
                                    <span v-else>-</span>
                                </li>
                                <li class="text-sm border-0 list-group-item ps-0">
                                    <strong class="text-dark">Email:</strong>&nbsp;
                                    <span v-if="company?.email !== '' "> {{ company?.email }}</span>
                                    <span v-else>-</span>
                                </li>
                                <li class="text-sm border-0 list-group-item ps-0">
                                    <strong class="text-dark">Account Manager:</strong>&nbsp;
                                    <span v-if="company?.registered_by !== '' "> {{ this.getAccountMngr(company.registered_by_id) }}</span>
                                    <span v-else>-</span>
                                </li>
                            </ul>
                        </div>
                        <div class="p-3 card-body row" v-if="edit">
                            <div class="col-6">
                                <div class="mb-3">
                                    <label for="name" class="form-label">İsim*</label>
                                    <input v-model="name" type="text" class="ps-0 form-control" id="name">
                                </div>
                                <div class="mb-3">
                                    <label for="phone" class="form-label">Telefon</label>
                                    <input v-model="phone" type="text" class="ps-0 form-control" id="phone">
                                </div>
                                <div class="mb-3">
                                    <label for="registered_by" class="form-label">Account Manager</label>
                                    <select v-model="registered_by" class="form-select" id="registered_by">
                                        <option value="null" selected>Kişi Seçin</option>
                                        <option v-for="user in users" :id="user.id" :value="user.id">{{ user.first_name }} {{ user.last_name }}</option>
                                    </select>
                                </div>
                                <button @click="submitEdit" type="submit" class="btn btn-primary">Güncelle</button>
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
                    <people-table v-if="this.exists" class="mt-3" :company_filter="company?.id ? company.id.toString() : '0'"/>
                    <projects-table v-if="this.exists" class="mt-3" :filter="company?.id ? company.id.toString() : '0'"/>

                </div>
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
import PeopleTable from "@/views/components/PeopleTable.vue";
import ProjectsTable from "@/views/components/ProjectsTable.vue";
import {axiosInstance} from "@/utils/utils";

export default {
    name: "ProjectCard",
    components: {
        VueSlider,
        PeopleTable,
        ProjectsTable
    },
    props: ['id'],

    data() {
        return {
            company: null,
            name: null,
            phone: null,
            email: null,
            address: null,
            edit: false,
            exists: false,
            registered_by: null,
            users: []
        }
    },
    async created() {
        try {
            const companyRes = await axiosInstance.get(`/kurumlar/${this.id}`);
            const usersRes = await axiosInstance.get(`/auth/kullanicilar`);
            this.exists = true

            this.users = usersRes.data.data
            this.company = companyRes.data.data
            this.registered_by = this.company.registered_by_id
        }
        catch (err){
            Swal.fire(
                'Hata',
                'Kurum Bulunamadı!',
                'error'
            ).then(async (result) => {
                if (result.isConfirmed) {
                    this.$router.push('/dashboard');

                }
            })

        }

    },
    computed: {},
    methods: {
        async submitEdit() {
            try {
                const response = await axiosInstance.put(`/kurumlar/${this.id}/`, {
                    name: this.name,
                    phone: this.phone,
                    email: this.email,
                    address: this.address,
                    registered_by: this.registered_by
                });

                Swal.fire(
                    'Güncellendi',
                    'Kurum/İş Ortağı Başarıyla Güncellendi!',
                    'success'
                );
                const companyRes = await axiosInstance.get(`/kurumlar/${this.id}`);
                this.company = companyRes.data.data

            } catch (err) {
                Swal.fire(
                    'Hata',
                    'Fırsat Güncellenemedi!',
                    'error'
                );
            }
            this.edit = false;
        },
        clickEdit() {
            this.edit = true
            this.name = this.company?.name
            this.phone = this.company?.phone
            this.email = this.company?.email
            this.address = this.company?.address
        },
        cancelEdit() {
            this.edit = false
            this.name = null
            this.phone = null
            this.email = null
            this.address = null
        },
        getAccountMngr(id) {
            const mngr = this.users.find(person => person.id === id)
            return mngr.first_name + " " + mngr.last_name
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
                cancelButtonText: 'İptal'
            }).then(async (result) => {
                if (result.isConfirmed) {
                    await axiosInstance.delete(`/kurumlar/${id}`);
                    if(this.company.role === 'client') {
                        this.$router.push('/companies')
                    }
                    else {
                        this.$router.push('/partners')
                    }
                }
            })
        },
    },

};
</script>
