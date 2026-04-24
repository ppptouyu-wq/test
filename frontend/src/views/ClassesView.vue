<template>
  <el-card shadow="never">
    <template #header>
      <div class="header">
        <span class="title">班级人数一览</span>
        <el-button text type="primary" @click="load">刷新</el-button>
      </div>
    </template>

    <el-table :data="rows" v-loading="loading" stripe style="width: 100%">
      <el-table-column prop="grade" label="年级" width="160" />
      <el-table-column prop="class_name" label="班级" width="160" />
      <el-table-column prop="count" label="学生人数" width="120" />
      <el-table-column label="操作" min-width="160">
        <template #default="{ row }">
          <el-button link type="primary" @click="goStudents(row)">查看该班学生</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-alert
      class="hint"
      type="info"
      :closable="false"
      show-icon
      title="「未填写」表示档案里对应字段为空，可在学生档案中补全年级、班级。"
    />
  </el-card>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { http } from "../api/http";

const router = useRouter();
const loading = ref(false);
const rows = ref([]);

async function load() {
  loading.value = true;
  try {
    const { data } = await http.get("/api/overview");
    rows.value = data.class_summary ?? [];
  } finally {
    loading.value = false;
  }
}

function goStudents(row) {
  const grade = row.grade === "未填写" ? "" : row.grade;
  const class_name = row.class_name === "未填写" ? "" : row.class_name;
  router.push({
    path: "/students",
    query: { grade: grade || undefined, class_name: class_name || undefined }
  });
}

onMounted(load);
</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.title {
  font-weight: 700;
}
.hint {
  margin-top: 16px;
}
</style>
