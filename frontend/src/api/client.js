import axios from "axios";

const apiBase = import.meta.env.VITE_API_BASE || "http://localhost:8000";

const client = axios.create({
  baseURL: apiBase,
  timeout: 15000,
});

client.interceptors.response.use(
  (res) => res,
  (err) => {
    const message = err.response?.data?.detail || err.message || "请求失败";
    console.error("API error:", message);
    return Promise.reject(new Error(message));
  },
);

export default client;
