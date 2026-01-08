<template>
  <div class="grid compute-layout">
    <section class="card">
      <header class="section-header">
        <div>
          <p class="muted">计算资源</p>
          <h2>云主机列表</h2>
        </div>
        <button @click="loadServers" :disabled="loading">刷新</button>
      </header>
      <table class="table">
        <thead>
          <tr>
            <th>名称</th>
            <th>状态</th>
            <th>镜像</th>
            <th>规格</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="srv in servers" :key="srv.id">
            <td>{{ srv.name }}</td>
            <td><span class="pill" :class="{ danger: srv.status !== 'ACTIVE' }">{{ srv.status }}</span></td>
            <td>{{ srv.image_id || "-" }}</td>
            <td>{{ srv.flavor_id || "-" }}</td>
            <td class="actions-row">
              <button class="ghost" @click="mutate(srv.id, 'start')">启动</button>
              <button class="ghost" @click="mutate(srv.id, 'stop')">关机</button>
              <button class="ghost" @click="mutate(srv.id, 'reboot', true)">重启</button>
              <button class="danger-btn" @click="removeServer(srv.id)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-if="!servers.length" class="muted">暂无云主机</p>
      <p v-if="error" class="muted">错误：{{ error }}</p>
    </section>

    <section class="card">
      <p class="muted">快速创建</p>
      <h2>新建云主机</h2>
      <form class="grid form" @submit.prevent="create">
        <label>
          名称
          <input v-model="form.name" placeholder="demo-vm" required />
        </label>
        <label>
          镜像
          <select v-model="form.image_id" required>
            <option value="" disabled>选择镜像</option>
            <option v-for="img in images" :key="img.id" :value="img.id">
              {{ img.name }} ({{ img.visibility || "private" }})
            </option>
          </select>
        </label>
        <label>
          规格
          <select v-model="form.flavor_id" required>
            <option value="" disabled>选择规格</option>
            <option v-for="flavor in flavors" :key="flavor.id" :value="flavor.id">
              {{ flavor.name }} - {{ flavor.vcpus }}vCPU / {{ flavor.ram_mb }}MB
            </option>
          </select>
        </label>
        <label>
          网络
          <select v-model="form.network_id" required>
            <option value="" disabled>选择网络</option>
            <option v-for="net in networks" :key="net.id" :value="net.id">
              {{ net.name || net.id }}
            </option>
          </select>
        </label>
        <label>
          SSH Key
          <input v-model="form.key_name" placeholder="可选" />
        </label>
        <label>
          安全组 (逗号分隔)
          <input v-model="sgInput" placeholder="default,web" />
        </label>
        <button type="submit" :disabled="creating">创建</button>
      </form>
      <p class="muted" v-if="createMessage">{{ createMessage }}</p>
    </section>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from "vue";
import { createServer, deleteServer, listFlavors, listImages, listNetworks, listServers, mutateServer } from "../api/openstack";

const servers = ref([]);
const flavors = ref([]);
const images = ref([]);
const networks = ref([]);
const error = ref("");
const loading = ref(false);
const creating = ref(false);
const createMessage = ref("");

const form = reactive({
  name: "",
  image_id: "",
  flavor_id: "",
  network_id: "",
  key_name: "",
  security_groups: [],
});

const sgInput = ref("");

const loadServers = async () => {
  loading.value = true;
  error.value = "";
  try {
    servers.value = await listServers();
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

const loadOptions = async () => {
  const [flv, imgs, nets] = await Promise.all([listFlavors(), listImages(), listNetworks()]);
  flavors.value = flv;
  images.value = imgs;
  networks.value = nets;
};

const create = async () => {
  creating.value = true;
  createMessage.value = "";
  form.security_groups = sgInput.value
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
  try {
    const res = await createServer({ ...form });
    createMessage.value = `创建成功：${res.name}`;
    await loadServers();
  } catch (err) {
    createMessage.value = `创建失败：${err.message}`;
  } finally {
    creating.value = false;
  }
};

const mutate = async (id, action, hard = false) => {
  try {
    await mutateServer(id, { action, hard });
    await loadServers();
  } catch (err) {
    error.value = err.message;
  }
};

const removeServer = async (id) => {
  if (!confirm("确认删除该云主机？")) return;
  try {
    await deleteServer(id);
    await loadServers();
  } catch (err) {
    error.value = err.message;
  }
};

onMounted(async () => {
  await Promise.all([loadServers(), loadOptions()]);
});
</script>

<style scoped>
.compute-layout {
  grid-template-columns: 2fr 1fr;
  align-items: start;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.actions-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.ghost {
  background: transparent;
  color: var(--text);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 8px 12px;
}

.danger-btn {
  background: var(--danger);
  color: #0b1724;
  border-radius: 10px;
  padding: 8px 12px;
}

.form {
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 12px;
}

label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  color: var(--muted);
  font-size: 14px;
}

@media (max-width: 900px) {
  .compute-layout {
    grid-template-columns: 1fr;
  }
}
</style>
