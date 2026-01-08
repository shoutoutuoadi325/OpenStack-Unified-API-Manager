<template>
  <div class="app-shell">
    <header class="topbar">
      <div class="brand">
        <span class="dot"></span>
        <div>
          <div class="title">OpenStack Unified Console</div>
          <div class="subtitle">FastAPI + Vue</div>
        </div>
      </div>
      <nav class="nav">
        <RouterLink to="/">仪表盘</RouterLink>
        <RouterLink to="/compute">计算</RouterLink>
        <RouterLink to="/network">网络</RouterLink>
        <RouterLink to="/storage">存储</RouterLink>
        <RouterLink to="/identity">身份</RouterLink>
      </nav>
    </header>
    <main class="page">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 20px;
  border-bottom: 1px solid var(--border);
  background: rgba(11, 23, 36, 0.85);
  backdrop-filter: blur(12px);
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  box-shadow: 0 0 0 8px rgba(42, 212, 163, 0.16);
}

.title {
  font-weight: 700;
  letter-spacing: 0.02em;
}

.subtitle {
  color: var(--muted);
  font-size: 12px;
}

.nav {
  display: flex;
  gap: 14px;
}

.nav a {
  padding: 8px 12px;
  border-radius: 12px;
  color: var(--text);
  transition: background 0.15s ease, color 0.15s ease;
}

.nav a.router-link-active {
  background: rgba(69, 160, 230, 0.18);
  color: #b9dcff;
}
</style>
