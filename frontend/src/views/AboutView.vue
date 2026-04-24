<template>
  <el-card shadow="never">
    <template #header><span class="title">关于本系统</span></template>

    <el-descriptions :column="1" border>
      <el-descriptions-item label="说明">
        教学演示用的学生信息管理：工作台汇总、学生档案 CRUD、班级人数统计、本页环境与接口自检。
      </el-descriptions-item>
      <el-descriptions-item label="技术栈">Flask REST API · Vue 3 · Vite · Element Plus · SQLAlchemy（SQLite / MySQL 可切换）</el-descriptions-item>
      <el-descriptions-item label="前端 API 基址">
        <code>{{ apiBase || "（同域，未设置 VITE_API_BASE）" }}</code>
      </el-descriptions-item>
      <el-descriptions-item label="后端健康检查">
        <el-space>
          <el-link :href="healthUrl" target="_blank" type="primary">{{ healthUrl }}</el-link>
          <el-tag v-if="healthOk === true" type="success" size="small">可达</el-tag>
          <el-tag v-else-if="healthOk === false" type="danger" size="small">不可达</el-tag>
          <el-button size="small" @click="pingHealth">检测</el-button>
        </el-space>
      </el-descriptions-item>
    </el-descriptions>
  </el-card>
</template>

<script setup>
import { computed, ref } from "vue";
import { http } from "../api/http";

const apiBase = import.meta.env.VITE_API_BASE || "";
const healthUrl = computed(() => (apiBase ? `${apiBase}/api/health` : "/api/health"));

const healthOk = ref(null);

async function pingHealth() {
  healthOk.value = null;
  try {
    const { data } = await http.get("/api/health", { timeout: 5000 });
    healthOk.value = !!(data && data.ok);
  } catch {
    healthOk.value = false;
  }
}
</script>

<style scoped>
.title {
  font-weight: 700;
}
code {
  font-size: 13px;
  word-break: break-all;
}
</style>
