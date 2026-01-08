import { createRouter, createWebHistory } from "vue-router";
import Dashboard from "../views/Dashboard.vue";
import Compute from "../views/Compute.vue";
import Network from "../views/Network.vue";
import Storage from "../views/Storage.vue";
import Identity from "../views/Identity.vue";

const routes = [
  { path: "/", name: "dashboard", component: Dashboard },
  { path: "/compute", name: "compute", component: Compute },
  { path: "/network", name: "network", component: Network },
  { path: "/storage", name: "storage", component: Storage },
  { path: "/identity", name: "identity", component: Identity },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
