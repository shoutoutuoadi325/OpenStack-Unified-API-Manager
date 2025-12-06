<template>
  <div class="page">
    <section class="hero card">
      <div>
        <p class="muted">统一视图</p>
        <h1>OpenStack API 管理台</h1>
        <p class="muted">在一个面板里管理计算、网络、存储与身份。Python + FastAPI 后端，Vue 前端。</p>
        <div class="actions">
          <RouterLink to="/compute"><button>开始创建云主机</button></RouterLink>
          <RouterLink to="/identity" class="ghost">查看项目</RouterLink>
        </div>
      </div>
    </section>

    <section class="grid stats">
      <StatCard label="云主机" :value="stats.servers" hint="Nova / Compute" />
      <StatCard label="块存储卷" :value="stats.volumes" hint="Cinder" />
      <StatCard label="对象存储桶" :value="stats.containers" hint="Swift" />
      <StatCard label="项目数" :value="stats.projects" hint="Keystone" />
    </section>

    <section v-if="error" class="card danger">
      <strong>加载失败：</strong> {{ error }}
    </section>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from "vue";
import { listContainers, listProjects, listServers, listVolumes } from "../api/openstack";
import StatCard from "../components/StatCard.vue";

const stats = reactive({
  servers: 0,
  volumes: 0,
  containers: 0,
  projects: 0,
});

const error = ref("");

const fetchStats = async () => {
  try {
    const [servers, volumes, containers, projects] = await Promise.all([
      listServers(),
      listVolumes(),
      listContainers(),
      listProjects(),
    ]);
    stats.servers = servers.length;
    stats.volumes = volumes.length;
    stats.containers = containers.length;
    stats.projects = projects.length;
  } catch (err) {
    error.value = err.message;
  }
};

onMounted(fetchStats);
</script>

<style scoped>
.hero h1 {
  margin: 6px 0 10px;
}

.actions {
  display: flex;
  gap: 12px;
  margin-top: 12px;
}

.ghost {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 14px;
  color: var(--text);
  border-radius: 10px;
  border: 1px solid var(--border);
  transition: background 0.15s ease;
}

.ghost:hover {
  background: rgba(255, 255, 255, 0.04);
}

.stats {
  margin-top: 18px;
  grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
}

.danger {
  border: 1px solid var(--danger);
  color: #ffb3b3;
}
</style>
