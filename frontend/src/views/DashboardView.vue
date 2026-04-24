<template>
  <div class="dashboard">
    <el-row :gutter="16">
      <el-col :xs="24" :sm="8">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-label">学生总数</div>
          <div class="stat-value">{{ overview.total }}</div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="8">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-label">年级分布（项）</div>
          <div class="stat-value">{{ overview.by_grade.length }}</div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="8">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-label">行政班（项）</div>
          <div class="stat-value">{{ overview.class_summary.length }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" class="row-block">
      <el-col :xs="24" :lg="12">
        <el-card shadow="never">
          <template #header><span class="card-title">按年级人数</span></template>
          <el-table :data="overview.by_grade" v-loading="loading" size="small" stripe>
            <el-table-column prop="grade" label="年级" />
            <el-table-column prop="count" label="人数" width="100" />
          </el-table>
        </el-card>
      </el-col>
      <el-col :xs="24" :lg="12">
        <el-card shadow="never">
          <template #header><span class="card-title">按性别</span></template>
          <el-table :data="overview.by_gender" v-loading="loading" size="small" stripe>
            <el-table-column prop="gender" label="性别" />
            <el-table-column prop="count" label="人数" width="100" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <el-card shadow="never" class="row-block">
      <template #header>
        <div class="card-head">
          <span class="card-title">快捷入口</span>
        </div>
      </template>
      <el-space wrap>
        <el-button type="primary" @click="$router.push('/students')">维护学生档案</el-button>
        <el-button @click="$router.push('/classes')">查看班级概览</el-button>
        <el-button @click="load">刷新数据</el-button>
      </el-space>
    </el-card>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from "vue";
import { http } from "../api/http";

const loading = ref(false);
const overview = reactive({
  total: 0,
  by_grade: [],
  by_gender: [],
  class_summary: []
});

async function load() {
  loading.value = true;
  try {
    const { data } = await http.get("/api/overview");
    overview.total = data.total ?? 0;
    overview.by_grade = data.by_grade ?? [];
    overview.by_gender = data.by_gender ?? [];
    overview.class_summary = data.class_summary ?? [];
  } finally {
    loading.value = false;
  }
}

onMounted(load);
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 0;
}
.stat-card {
  margin-bottom: 16px;
}
.stat-label {
  font-size: 13px;
  color: #6b7280;
}
.stat-value {
  margin-top: 8px;
  font-size: 28px;
  font-weight: 700;
  color: #111827;
}
.row-block {
  margin-top: 0;
}
.row-block + .row-block {
  margin-top: 16px;
}
.card-title {
  font-weight: 600;
}
.card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>
