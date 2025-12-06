<template>
  <div class="grid storage-layout">
    <section class="card">
      <header class="section-header">
        <div>
          <p class="muted">块存储</p>
          <h2>卷列表</h2>
        </div>
        <button @click="loadVolumes">刷新</button>
      </header>
      <table class="table">
        <thead>
          <tr>
            <th>名称</th>
            <th>状态</th>
            <th>大小(GiB)</th>
            <th>挂载</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="vol in volumes" :key="vol.id">
            <td>{{ vol.name || vol.id }}</td>
            <td><span class="pill" :class="{ danger: vol.status !== 'available' }">{{ vol.status }}</span></td>
            <td>{{ vol.size }}</td>
            <td>{{ vol.attachments?.length || 0 }}</td>
            <td><button class="danger-btn" @click="removeVolume(vol.id)">删除</button></td>
          </tr>
        </tbody>
      </table>
      <p v-if="!volumes.length" class="muted">暂无卷</p>
    </section>

    <section class="card">
      <p class="muted">新建卷</p>
      <h2>快速创建</h2>
      <form class="grid form" @submit.prevent="create">
        <label>
          名称
          <input v-model="form.name" placeholder="data-volume" />
        </label>
        <label>
          大小 (GiB)
          <input v-model.number="form.size" type="number" min="1" required />
        </label>
        <label>
          描述
          <input v-model="form.description" placeholder="可选" />
        </label>
        <button type="submit">创建卷</button>
      </form>
      <p class="muted" v-if="message">{{ message }}</p>
    </section>

    <section class="card">
      <header class="section-header">
        <div>
          <p class="muted">对象存储</p>
          <h2>容器</h2>
        </div>
        <button @click="loadContainers">刷新</button>
      </header>
      <div class="grid containers">
        <div v-for="ct in containers" :key="ct.name" class="container-card" @click="selectContainer(ct.name)">
          <div class="label">{{ ct.name }}</div>
          <div class="muted">{{ ct.count || 0 }} 对象</div>
        </div>
      </div>
      <div v-if="selectedContainer" class="objects">
        <h3>对象 - {{ selectedContainer }}</h3>
        <ul>
          <li v-for="obj in objects" :key="obj.name">
            {{ obj.name }} <span class="muted">({{ obj.bytes }} bytes)</span>
          </li>
        </ul>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from "vue";
import { createVolume, deleteVolume, listContainers, listObjects, listVolumes } from "../api/openstack";

const volumes = ref([]);
const containers = ref([]);
const objects = ref([]);
const selectedContainer = ref("");
const form = reactive({
  name: "",
  size: 1,
  description: "",
});
const message = ref("");

const loadVolumes = async () => {
  volumes.value = await listVolumes();
};

const create = async () => {
  try {
    await createVolume({ ...form });
    message.value = "创建成功";
    await loadVolumes();
  } catch (err) {
    message.value = `创建失败：${err.message}`;
  }
};

const removeVolume = async (id) => {
  if (!confirm("确认删除该卷？")) return;
  await deleteVolume(id);
  await loadVolumes();
};

const loadContainers = async () => {
  containers.value = await listContainers();
};

const selectContainer = async (name) => {
  selectedContainer.value = name;
  objects.value = await listObjects(name);
};

onMounted(async () => {
  await Promise.all([loadVolumes(), loadContainers()]);
});
</script>

<style scoped>
.storage-layout {
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 18px;
}

.form {
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}

.containers {
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
}

.container-card {
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: 12px;
  background: var(--panel-strong);
  cursor: pointer;
  transition: border 0.15s ease, transform 0.15s ease;
}

.container-card:hover {
  border-color: var(--accent);
  transform: translateY(-2px);
}

.label {
  font-weight: 600;
}

.objects ul {
  padding-left: 16px;
}

.danger-btn {
  background: var(--danger);
  color: #0b1724;
  border-radius: 10px;
  padding: 8px 12px;
}
</style>
