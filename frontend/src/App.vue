<template>
  <div class="app">
    <header class="topbar">
      <div class="brand">学生管理系统</div>
      <div class="hint">Flask + Vue + Element Plus</div>
    </header>

    <el-container class="layout">
      <el-aside width="220px" class="aside">
        <el-menu :default-active="activeMenu" router class="menu">
          <el-menu-item index="/">
            <span>工作台</span>
          </el-menu-item>
          <el-menu-item index="/students">
            <span>学生档案</span>
          </el-menu-item>
          <el-menu-item index="/classes">
            <span>班级概览</span>
          </el-menu-item>
          <el-menu-item index="/about">
            <span>关于</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const activeMenu = computed(() => (route.path === "/" ? "/" : route.path));
</script>

<style scoped>
.app {
  min-height: 100vh;
  background: #f5f7fb;
}
.topbar {
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 18px;
  background: #111827;
  color: #fff;
}
.brand {
  font-weight: 700;
  letter-spacing: 0.5px;
}
.hint {
  opacity: 0.8;
  font-size: 12px;
}
.layout {
  max-width: 1280px;
  margin: 0 auto;
  min-height: calc(100vh - 56px);
  background: #f5f7fb;
}
.aside {
  background: #fff;
  border-right: 1px solid #e5e7eb;
}
.menu {
  border-right: none;
  padding-top: 12px;
}
.main {
  padding: 18px;
  background: #f5f7fb;
}
</style>
