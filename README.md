# OpenStack Unified API Manager

> FastAPI + Vue 控制台，在单一界面下统一管理计算（Nova）、身份（Keystone）、镜像（Glance）、网络（Neutron）、对象存储（Swift）、块存储（Cinder）。

## 架构概要
- **后端**：Python / FastAPI，使用 `openstacksdk` 连接各 OpenStack 服务；按服务拆分路由模块（`/compute`, `/identity`, `/images`, `/network`, `/object-storage`, `/block-storage`）。
- **配置**：`.env` 读取标准的 `OS_*` 环境变量（示例见 `backend/.env.example`），通过 `pydantic-settings` 注入。
- **前端**：Vue 3 + Vite + Axios，提供仪表盘、计算、网络、存储、身份视图，调用后端 REST 接口。

目录结构：
```
backend/
  app/
    main.py                 # FastAPI 入口
    config.py               # 环境配置
    dependencies/openstack.py
    routers/                # 各服务路由
    schemas.py
  requirements.txt
  .env.example
frontend/
  src/ (App.vue, views, api/)
  package.json
  .env.example
```

## 快速开始
### 1) 准备 OpenStack 认证信息
复制并修改 `backend/.env.example` 为 `backend/.env`，填入 Keystone 认证地址、用户名、密码、项目、域等。

### 2) 启动后端（FastAPI）
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows 使用 .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --app-dir .
```
默认监听 `http://localhost:8000`，Swagger 文档位于 `/docs`。

### 3) 启动前端（Vue）
```bash
cd frontend
npm install
cp .env.example .env   # 如需修改后端地址请调整 VITE_API_BASE
npm run dev
```
访问 `http://localhost:5173`。

## 已覆盖的核心 API
- **计算（Nova）**：列出/查询云主机，创建、启动、停止、重启、删除；列出规格。
- **身份（Keystone）**：列出项目、用户。
- **镜像（Glance）**：列出/查询镜像。
- **网络（Neutron）**：列出网络、子网、安全组。
- **对象存储（Swift）**：列出/创建容器，列出对象。
- **块存储（Cinder）**：列出/查询/创建/删除卷。

## 后续可扩展项
1. 为创建云主机增加可选参数：端口、浮动 IP、元数据、云配置。
2. 接入认证令牌缓存/刷新与角色判断，细化 RBAC。
3. 在前端补充操作反馈、轮询任务进度、表格分页与搜索。
4. 为对象存储增加上传/下载、容器 ACL 管理。
5. 增加自动化测试（FastAPI 路由单测 + 前端组件单测）。

