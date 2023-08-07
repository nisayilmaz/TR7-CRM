<template>
    <div class="card mb-4">
        <div v-if="found" class="container">
            <div class="row">

                <div class="mt-4 col-md-12 col-xl-12 mt-md-0">
                    <project-card @updated-proj="(proj) => this.project = proj" :project="project"/>
                </div>
            </div>

            <div class="mt-4 row">

                <div class="col-12">
                    <div class="mb-4 card">
                        <div class="p-3 pb-0 card-header">
<!--                            <h6 class="mb-1">Notlar</h6>-->
                            <nav-pill @variable-changed="handleFilter"/>

                            <div class="accordion accordion-flush" id="addNoteAccordion">
                                <div class="accordion-item">
                                    <h4 class="accordion-header">
                                        <button class="ps-0 accordion-button collapsed " type="button" data-bs-toggle="collapse"
                                                data-bs-target="#addNote" aria-expanded="false" aria-controls="flush-collapseOne">
                                            Not Ekle <i class="fa fa-plus ms-2" aria-hidden="true"></i>
                                        </button>
                                    </h4>
                                    <div id="addNote" class="accordion-collapse collapse" data-bs-parent="#addNoteAccordion">
                                        <div class="accordion-body">
                                            <form class="row">
                                                <div class="col-4">
                                                    <div class="mb-3">
                                                        <label for="title" class="form-label">Başlık*</label>
                                                        <input v-model="title" type="text" class="ps-0 form-control" id="title">
                                                    </div>
                                                    <div class="mb-3">
                                                        <label for="note" class="form-label">Not*</label>
                                                        <input v-model="note" type="text" class="ps-0 form-control" id="note">
                                                    </div>
                                                    <div class="mb-3">
                                                        <label for="type" class="form-label">Kategori*</label>
                                                        <select v-model="type" class="form-select" id="partner">
                                                            <option value="1">Arama</option>
                                                            <option value="2">Yüzyüze Görüşme</option>
                                                            <option value="3">İş Ortağı İle Görüşme</option>
                                                            <option value="4">E-posta</option>
                                                            <option value="5">Genel</option>
                                                            <option value="6">Etkinlik</option>
                                                            <option value="7">İş Yemeği</option>
                                                            <option value="8">Diğer</option>
                                                        </select>
                                                    </div>
                                                </div>
                                            </form>
                                            <button @click="addNote" type="submit" class="btn btn-primary">Ekle</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="card-body pt-4 p-3">
                            <ul class="list-group">
                                <li v-for="note in filteredNotes" :key="note.id" class="list-group-item border-0 d-flex p-4 mb-2 bg-gray-100 border-radius-lg">
                                    <div class="d-flex flex-column">
                                        <h6 class="mb-3 text-sm">{{note.title}}</h6>
                                        <span class="mb-2 text-xs">Tarih:
                                            <span class="text-dark font-weight-bold ms-sm-2">{{formatDate(note.creation_date)}}</span>
                                        </span>
                                        <span class="mb-2 text-xs">
                                              Kategori:
                                              <span class="text-dark ms-sm-2 font-weight-bold">{{formatCategory(note.category)}}</span>
                                        </span>
                                        <span class="text-xs">
                                              Not:
                                              <span class="text-dark ms-sm-2 font-weight-bold">{{note.note}}</span>
                                        </span>
                                    </div>
                                    <div class="ms-auto text-end">
                                        <a @click="deleteNote($event ,note.id)" class="btn btn-link text-danger text-gradient px-3 mb-0" >
                                            <i class="far fa-trash-alt me-2" aria-hidden="true"></i>
                                        </a>
                                    </div>
                                </li>

                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import VsudSwitch from "@/components/VsudSwitch.vue";
import ProfileCard from "./components/ProjectCard.vue";
import VsudAvatar from "../components/VsudAvatar.vue";
import ProjectsCard from "./components/ProjectOverviewCard.vue";
import axios from "axios";
import ProjectCard from "@/views/components/ProjectCard.vue";
import Swal from "sweetalert2";
import NavPill from "./components/NavPill.vue";
import moment from "moment";
import {axiosInstance} from "@/utils/utils";

export default {
    name: "ProjectDetail",
    components: {
        VsudSwitch,
        VsudAvatar,
        ProjectsCard,
        ProjectCard,
        NavPill
    },
    props: ['id'],

    data() {
        return {
            project : {},
            notes: [],
            filteredNotes: [],
            note: "",
            title:"",
            type: "",
            found: false
        };
    },
    async created() {
        try {
            const projectsRes = await axiosInstance.get(`/firsatlar/${this.id}`);
            this.project = projectsRes.data.data

            const notesRes = await axiosInstance.get(`/notlar/${this.id}`);
            this.found = true
            this.notes = notesRes.data.data
            this.filteredNotes = notesRes.data.data
        }catch (err) {
            Swal.fire(
                'Hata',
                'Fırsat Bulunamadı!',
                'error'
            ).then(async (result) => {
                if (result.isConfirmed) {
                    this.$router.push('/dashboard');

                }
            })
        }
    },
    methods : {
        handleFilter(newFilter){
            if(newFilter === 0) {
                this.filteredNotes = this.notes
            }
            else {
                this.filteredNotes = this.notes.filter(note => note.category === newFilter)

            }
        },
        deleteNote(e,noteId) {
            e.preventDefault();
            Swal.fire({
                title: 'Bu notu silmek istediğinize emin misiniz?',
                text: "",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sil',
                cancelButtonText:'İptal'
            }).then(async (result) => {
                if (result.isConfirmed) {
                    await axiosInstance.delete(`/notlar/${noteId}`);
                    this.filteredNotes = this.filteredNotes.filter(note => note.id !== noteId);

                }
            })
        },
        formatDate(date, format = "DD.MM.YYYY") {
            if(date === null) {
                return null
            }
            return moment(date).format(format)
        },
        formatCategory(category) {
            const categories = ["","Arama", "Yüzyüze Görüşme", "İş Ortağı İle Görüşme", "E-posta"]
            return categories[category]
        },
        async addNote(e) {
            e.preventDefault()
            try {
                const response = await axiosInstance.post(`/notlar/`, {
                    title: this.title,
                    note: this.note,
                    project: this.project.id,
                    category: this.type
                });
                if(response.data.data){
                    this.notes.splice(0, 0, response.data.data);
                    this.notes.join()
                    Swal.fire(
                        'Not Başarıyla Eklendi',
                        '',
                        'success'
                    )

                    this.title = ""
                    this.note = ""
                    this.type = ""
                }
            }catch (err) {
                Swal.fire(
                    'Hata',
                    'Not Eklenemedi!',
                    'error'
                )
            }
        },
    }
};
</script>
