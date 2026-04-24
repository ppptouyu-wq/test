import { createRouter, createWebHistory } from "vue-router";

import DashboardView from "../views/DashboardView.vue";
import StudentsView from "../views/StudentsView.vue";
import ClassesView from "../views/ClassesView.vue";
import AboutView from "../views/AboutView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", name: "dashboard", component: DashboardView, meta: { title: "工作台" } },
    { path: "/students", name: "students", component: StudentsView, meta: { title: "学生档案" } },
    { path: "/classes", name: "classes", component: ClassesView, meta: { title: "班级概览" } },
    { path: "/about", name: "about", component: AboutView, meta: { title: "关于" } }
  ]
});

router.afterEach((to) => {
  const base = to.meta.title || "学生管理系统";
  document.title = `${base} · 学生管理系统`;
});

export default router;
