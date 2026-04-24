<template>
  <el-card shadow="never">
    <template #header>
      <div class="header">
        <div class="title">学生列表</div>
        <div class="actions">
          <el-input
            v-model="filters.q"
            placeholder="按姓名/学号搜索"
            clearable
            style="width: 220px"
            @keyup.enter="reload"
          />
          <el-input v-model="filters.grade" placeholder="年级" clearable style="width: 140px" />
          <el-input v-model="filters.class_name" placeholder="班级" clearable style="width: 140px" />
          <el-button type="primary" @click="reload">查询</el-button>
          <el-button @click="openCreate">新增</el-button>
        </div>
      </div>
    </template>

    <el-table :data="items" v-loading="loading" style="width: 100%">
      <el-table-column prop="student_no" label="学号" width="140" />
      <el-table-column prop="name" label="姓名" width="140" />
      <el-table-column prop="gender" label="性别" width="90" />
      <el-table-column prop="birth_date" label="出生日期" width="130" />
      <el-table-column prop="grade" label="年级" width="120" />
      <el-table-column prop="class_name" label="班级" width="120" />
      <el-table-column prop="phone" label="电话" min-width="140" />
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="openEdit(row)">编辑</el-button>
          <el-popconfirm title="确认删除该学生？" @confirm="remove(row)">
            <template #reference>
              <el-button link type="danger">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <div class="pager">
      <el-pagination
        background
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        :page-size="pageSize"
        :current-page="page"
        :page-sizes="[10, 20, 50, 100]"
        @update:current-page="onPageChange"
        @update:page-size="onSizeChange"
      />
    </div>
  </el-card>

  <el-dialog v-model="dialog.open" :title="dialog.mode === 'create' ? '新增学生' : '编辑学生'" width="560px">
    <el-form :model="dialog.form" label-width="90px">
      <el-form-item label="学号" required>
        <el-input v-model="dialog.form.student_no" />
      </el-form-item>
      <el-form-item label="姓名" required>
        <el-input v-model="dialog.form.name" />
      </el-form-item>
      <el-form-item label="性别">
        <el-select v-model="dialog.form.gender" clearable placeholder="请选择">
          <el-option label="男" value="男" />
          <el-option label="女" value="女" />
          <el-option label="其他" value="其他" />
        </el-select>
      </el-form-item>
      <el-form-item label="出生日期">
        <el-date-picker v-model="dialog.form.birth_date" type="date" value-format="YYYY-MM-DD" />
      </el-form-item>
      <el-form-item label="年级">
        <el-input v-model="dialog.form.grade" />
      </el-form-item>
      <el-form-item label="班级">
        <el-input v-model="dialog.form.class_name" />
      </el-form-item>
      <el-form-item label="电话">
        <el-input v-model="dialog.form.phone" />
      </el-form-item>
      <el-form-item label="邮箱">
        <el-input v-model="dialog.form.email" />
      </el-form-item>
      <el-form-item label="地址">
        <el-input v-model="dialog.form.address" type="textarea" :rows="2" />
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="dialog.open = false">取消</el-button>
      <el-button type="primary" :loading="dialog.saving" @click="save">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { onMounted, reactive, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { ElMessage } from "element-plus";
import { http } from "../api/http";

const route = useRoute();

const loading = ref(false);
const items = ref([]);
const total = ref(0);

const page = ref(1);
const pageSize = ref(10);

const filters = reactive({
  q: "",
  grade: "",
  class_name: ""
});

const dialog = reactive({
  open: false,
  mode: "create",
  saving: false,
  id: null,
  form: {
    student_no: "",
    name: "",
    gender: "",
    birth_date: "",
    grade: "",
    class_name: "",
    phone: "",
    email: "",
    address: ""
  }
});

function resetForm() {
  dialog.form = {
    student_no: "",
    name: "",
    gender: "",
    birth_date: "",
    grade: "",
    class_name: "",
    phone: "",
    email: "",
    address: ""
  };
}

function syncFiltersFromRoute() {
  const q = route.query;
  filters.q = typeof q.q === "string" ? q.q : "";
  filters.grade = typeof q.grade === "string" ? q.grade : "";
  filters.class_name = typeof q.class_name === "string" ? q.class_name : "";
}

async function reload() {
  loading.value = true;
  try {
    const res = await http.get("/api/students", {
      params: {
        page: page.value,
        page_size: pageSize.value,
        q: filters.q || undefined,
        grade: filters.grade || undefined,
        class_name: filters.class_name || undefined
      }
    });
    items.value = res.data.items;
    total.value = res.data.total;
  } finally {
    loading.value = false;
  }
}

function onPageChange(p) {
  page.value = p;
  reload();
}

function onSizeChange(ps) {
  pageSize.value = ps;
  page.value = 1;
  reload();
}

function openCreate() {
  dialog.mode = "create";
  dialog.id = null;
  resetForm();
  dialog.open = true;
}

function openEdit(row) {
  dialog.mode = "edit";
  dialog.id = row.id;
  dialog.form = {
    student_no: row.student_no || "",
    name: row.name || "",
    gender: row.gender || "",
    birth_date: row.birth_date || "",
    grade: row.grade || "",
    class_name: row.class_name || "",
    phone: row.phone || "",
    email: row.email || "",
    address: row.address || ""
  };
  dialog.open = true;
}

async function save() {
  if (!dialog.form.student_no?.trim() || !dialog.form.name?.trim()) {
    ElMessage.error("学号和姓名必填");
    return;
  }
  dialog.saving = true;
  try {
    if (dialog.mode === "create") {
      await http.post("/api/students", dialog.form);
      ElMessage.success("新增成功");
    } else {
      await http.put(`/api/students/${dialog.id}`, dialog.form);
      ElMessage.success("保存成功");
    }
    dialog.open = false;
    await reload();
  } catch (e) {
    const msg = e?.response?.data?.message || "请求失败";
    ElMessage.error(msg);
  } finally {
    dialog.saving = false;
  }
}

async function remove(row) {
  try {
    await http.delete(`/api/students/${row.id}`);
    ElMessage.success("删除成功");
    if (items.value.length === 1 && page.value > 1) page.value -= 1;
    await reload();
  } catch (e) {
    const msg = e?.response?.data?.message || "删除失败";
    ElMessage.error(msg);
  }
}

onMounted(() => {
  syncFiltersFromRoute();
  reload();
});

watch(
  () => route.query,
  () => {
    syncFiltersFromRoute();
    page.value = 1;
    reload();
  },
  { deep: true }
);
</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}
.title {
  font-weight: 700;
}
.actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: flex-end;
}
.pager {
  display: flex;
  justify-content: flex-end;
  margin-top: 14px;
}
</style>

