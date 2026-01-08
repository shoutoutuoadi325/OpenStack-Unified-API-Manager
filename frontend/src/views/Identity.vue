<template>
  <div class="grid identity-layout">
    <section class="card">
      <header class="section-header">
        <div>
          <p class="muted">项目</p>
          <h2>Projects</h2>
        </div>
        <button @click="loadProjects">刷新</button>
      </header>
      <table class="table">
        <thead>
          <tr>
            <th>名称</th>
            <th>描述</th>
            <th>状态</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="project in projects" :key="project.id">
            <td>{{ project.name }}</td>
            <td>{{ project.description }}</td>
            <td><span class="pill" :class="{ danger: !project.enabled }">{{ project.enabled ? "启用" : "禁用" }}</span></td>
          </tr>
        </tbody>
      </table>
    </section>

    <section class="card">
      <header class="section-header">
        <div>
          <p class="muted">用户</p>
          <h2>Users</h2>
        </div>
        <button @click="loadUsers">刷新</button>
      </header>
      <table class="table">
        <thead>
          <tr>
            <th>名称</th>
            <th>邮箱</th>
            <th>默认项目</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.name }}</td>
            <td>{{ user.email || "-" }}</td>
            <td>{{ user.default_project_id || "-" }}</td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { listProjects, listUsers } from "../api/openstack";

const projects = ref([]);
const users = ref([]);

const loadProjects = async () => {
  projects.value = await listProjects();
};

const loadUsers = async () => {
  users.value = await listUsers();
};

onMounted(async () => {
  await Promise.all([loadProjects(), loadUsers()]);
});
</script>

<style scoped>
.identity-layout {
  grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
  gap: 18px;
}
</style>
