import {createRouter, createWebHashHistory, createWebHistory} from "vue-router";
import Dashboard from "@/views/Dashboard.vue";
import SignIn from "@/views/SignIn.vue";
import Projects from "@/views/Projects.vue";
import Companies from "@/views/Companies.vue";
import Partners from "@/views/Partners.vue";
import People from "@/views/People.vue";
import Users from "@/views/Users.vue";
import ProjectDetail from "@/views/ProjectDetail.vue";
import FinishedProjects from "@/views/FinishedProjects.vue";
import CompanyDetail from "@/views/components/CompanyDetail.vue";
import ClosedProjects from "@/views/ClosedProjects.vue";
import LostProjects from "@/views/LostProjects.vue";
import VirtualReality from "@/views/VirtualReality.vue";
import SignUp from "@/views/SignUp.vue";

const routes = [
  {
    path: "/",
    name: "/",
    redirect: "/log-in",
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: Dashboard,
    meta: {
      requiresAuth: true
    }
  },
  {
    //Todo: Kurumun ingilizcesi?
    path: "/companies",
    name: "Companies",
    component: Companies,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: "/partners",
    name: "Partners",
    component: Partners,
    meta: {
      requiresAuth: true
    }
  },
  {
    //Todo: firsatın ingilizcesi???
    path: "/opportunities",
    name: "Projects",
    component: Projects,
    meta: {
      requiresAuth: true
    }
  },
  {
    //Todo: firsatın ingilizcesi???

    path: "/gerceklesen-firsatlar",
    name: "FinishedProjects",
    component: FinishedProjects,
    meta: {
      requiresAuth: true
    }
  },
  {
    //Todo: firsatın ingilizcesi???

    path: "/kapanan-firsatlar",
    name: "ClosedProjects",
    component: ClosedProjects,
    meta: {
      requiresAuth: true
    },
    props: true

  },
  {
    //Todo: firsatın ingilizcesi???

    path: "/kaybedilen-firsatlar",
    name: "LostProjects",
    component: LostProjects,
    meta: {
      requiresAuth: true
    },
    props: true

  },
  {
    path: "/people",
    name: "People",
    component: People,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: "/accounts",
    name: "Users",
    component: Users,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: "/log-in",
    name: "Log In",
    component: SignIn,
  },
  {
    path: "/opportunity/:id",
    name: "ProjectDetail",
    component: ProjectDetail,
    props: true

  },
  {
    path: "/company/:id",
    name: "CompanyDetail",
    component: CompanyDetail,
    props: true

  },
  {
    path: "/api/:id",
    name: "CompanyDetail",
    component: CompanyDetail,
    props: true

  },
  {
    path: "/password_reset/:token",
    name: "PasswordReset",
    component: SignUp,
    meta: {
      requiresAuth: false // Adjust the meta data as needed for this route
    }
  }
];
//
// const router = createRouter({
//   history: createWebHistory(import.meta.env.BASE_URL),
//   routes,
//   linkActiveClass: "active",
// });
const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes,
  linkActiveClass: "active",
});


export default router;
