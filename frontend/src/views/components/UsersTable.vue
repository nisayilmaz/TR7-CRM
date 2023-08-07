<template>
    <div class="card mb-4 users-table" :style="mainStyle">
        <div class="card-header pb-0">
            <h6>Kullanıcılar</h6>
            <div class="accordion accordion-flush" id="accordionFlushExample">
                <div class="accordion-item">
                    <h4 class="accordion-header">
                        <button class="ps-0 accordion-button collapsed " type="button" data-bs-toggle="collapse"
                                data-bs-target="#addUser" aria-expanded="false" aria-controls="flush-collapseOne">
                            Kullanıcı Ekle <i class="fa fa-plus ms-2" aria-hidden="true"></i>
                        </button>
                    </h4>
                    <div id="addUser" class="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                        <div class="accordion-body">
                            <form class="row">
                                <div class="col-4">
                                    <div class="mb-3">
                                        <label for="name" class="form-label">Ad*</label>
                                        <input v-model="first_name" type="text" class="ps-0 form-control" id="name">
                                    </div>
                                    <div class="mb-3">
                                        <label for="surname" class="form-label">Soyad*</label>
                                        <input v-model="last_name" type="text" class="ps-0 form-control" id="surname">
                                    </div>
                                    <div class="mb-3">
                                        <label for="email" class="form-label">Email*</label>
                                        <input v-model="email" type="text" class="ps-0 form-control" id="email">
                                    </div>
                                </div>
                                <div class="col-4">
                                    <div class="mb-4">
                                        <label for="role" class="form-label">Rol*</label>
                                        <select id="role" v-model="role" class="form-select"  >
                                            <option value="null" selected>Rol Seçin</option>
                                            <option value="1">Admin</option>
                                            <option value="2">Account Manager</option>
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label for="password" class="form-label">Şifre*</label>
                                        <input v-model="password" type="text" class="ps-0 form-control" id="password">
                                    </div>
                                </div>
                            </form>
                            <button @click="addUser" v-if="response" type="submit" class="btn btn-primary">Ekle</button>
                            <div v-if="!response" class="spinner-border ms-2" role="status">
                                <span class="sr-only">Loading...</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="card-body px-0 pt-0 pb-2">
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
                            Rol
                        </th>
                        <th></th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-for="user in users" :key="user.id">
                        <td>
                            <div class="d-flex px-2">
                                <div class="my-auto">
                                    <h6 class="mb-0 text-sm">{{user.first_name}}</h6>
                                </div>
                            </div>
                        </td>
                        <td>
                            <p class="text-sm font-weight-bold mb-0">{{user.last_name}}</p>
                        </td>
                        <td>
                            <span class="text-xs font-weight-bold">{{user.email}}</span>
                        </td>
                        <td>
                            <span class="text-xs font-weight-bold">{{getRole(user?.role)}}</span>
                        </td>
                        <td>
                            <a class="btn btn-link text-danger text-gradient px-3 mb-0" href="javascript:;">
                                <i @click="this.deletePerson($event,user.id)"
                                   class="far fa-trash-alt me-2" aria-hidden="true"></i>
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
import vsudAlert from "@/components/VsudAlert.vue";
import {axiosInstance} from "@/utils/utils";
import Swal from "sweetalert2";
export default {
    name: "UsersTable",
    components: {
        vsudAlert
    },
    computed: {
        mainStyle() {
            return {
                opacity: this.loading ? 0 : 1
            }
        },
    },
    data() {
        return {
            companies : [],
            users: [],
            first_name : "",
            last_name : "",
            role: null,
            email: "",
            password: "",
            loading : true,
            response : true
        }
    },
    async created() {
        this.loading = true
        const companiesRes = await axiosInstance.get(`/kurumlar/`);
        if (companiesRes.data.status === "success") {
            this.companies = companiesRes.data.data;
        }

        try {
            const usersRes = await axiosInstance.get(`/auth/kullanicilar`);
            this.users = usersRes.data.data
        }
        catch (err) {
        }
        this.loading = false

    },
    methods: {
        async addUser(e) {
            try {
                e.preventDefault();
                this.response = false
                const resp = await axiosInstance.post(`/auth/register/`, {
                    password: this.password,
                    email: this.email,
                    role: this.role,
                    first_name : this.first_name,
                    last_name : this.last_name
                });
                const personToAdd = resp.data.user
                const index = this.users.findIndex(user => personToAdd.first_name.localeCompare(user.first_name) < 0);
                const insertIndex = index === -1 ? this.users.length : index;
                this.users.splice(insertIndex, 0, personToAdd);
                Swal.fire(
                    'Kullanıcı Başarıyla Eklendi',
                    '',
                    'success'
                )
                this.response = true
                await axiosInstance.post(`/mailer/`, {
                    email : this.email,
                    password : this.password
                });

            }
            catch (err){
                this.response = true
            }
            this.email = "";
            this.password = "";
            this.first_name = ""
            this.last_name = ""
            this.company = ""
            this.role = null
        },
        getCompanyName(companyId) {
            if(!Array.isArray(this.companies)) return " "
            const comp = this.companies.find(c => c.id === companyId);
            return comp ? comp.name : " ";
        },
        getRole(role) {
            if(role === "" || role === null) {
                return ""
            }
            else {
                if(role === 1) {
                    return "Admin"
                }
                else if (role === 2) {
                    return "Account Manager"
                }
                else {
                    return ""
                }
            }
        },
        async deletePerson(e, id) {
            e.preventDefault();
            try {
                e.preventDefault();
                Swal.fire({
                    title: 'Bu hesabı silmek istediğinize emin misiniz?',
                    text: "Bu işlem geri alınamaz ve hesapla ilişkili tüm fırsatlar da silinir.",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'Sil',
                    cancelButtonText: 'İptal'
                }).then(async (result) => {
                    if (result.isConfirmed) {
                        await axiosInstance.delete(`/auth/kullanicilar/${id}`);
                        this.users = this.users.filter(person => person.id !== id);
                        this.$router.push("/accounts")
                    }
                })
            }
            catch (err) {
            }
        },
    },
};
</script>


<style lang="scss">
.users-table{
    transition: opacity linear 0.1s;
}
</style>