<template>
  <div class="grid">
    <section class="card">
      <header class="section-header">
        <div>
          <p class="muted">网络</p>
          <h2>网络列表</h2>
        </div>
        <button @click="loadNetworks">刷新</button>
      </header>
      <table class="table">
        <thead>
          <tr>
            <th>名称</th>
            <th>状态</th>
            <th>共享</th>
            <th>外部</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="net in networks" :key="net.id">
            <td>{{ net.name || net.id }}</td>
            <td><span class="pill" :class="{ danger: net.status !== 'ACTIVE' }">{{ net.status }}</span></td>
            <td>{{ net.shared ? "是" : "否" }}</td>
            <td>{{ net.external ? "是" : "否" }}</td>
          </tr>
        </tbody>
      </table>
    </section>

    <section class="card">
      <header class="section-header">
        <div>
          <p class="muted">安全组</p>
          <h2>Security Groups</h2>
        </div>
        <button @click="loadSecurityGroups">刷新</button>
      </header>
      <table class="table">
        <thead>
          <tr>
            <th>名称</th>
            <th>描述</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sg in securityGroups" :key="sg.id">
            <td>{{ sg.name }}</td>
            <td>{{ sg.description }}</td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { listNetworks, listSecurityGroups } from "../api/openstack";

const networks = ref([]);
const securityGroups = ref([]);

const loadNetworks = async () => {
  networks.value = await listNetworks();
};

const loadSecurityGroups = async () => {
  securityGroups.value = await listSecurityGroups();
};

onMounted(async () => {
  await Promise.all([loadNetworks(), loadSecurityGroups()]);
});
</script>

<style scoped>
.grid {
  grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
}
</style>
