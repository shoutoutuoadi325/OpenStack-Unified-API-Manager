import client from "./client";

export const listServers = () => client.get("/compute/servers").then((r) => r.data);
export const createServer = (payload) => client.post("/compute/servers", payload).then((r) => r.data);
export const mutateServer = (id, payload) => client.post(`/compute/servers/${id}/actions`, payload).then((r) => r.data);
export const deleteServer = (id) => client.delete(`/compute/servers/${id}`).then((r) => r.data);
export const listFlavors = () => client.get("/compute/flavors").then((r) => r.data);

export const listImages = () => client.get("/images").then((r) => r.data);

export const listNetworks = () => client.get("/network/networks").then((r) => r.data);
export const listSecurityGroups = () => client.get("/network/security-groups").then((r) => r.data);

export const listVolumes = () => client.get("/block-storage/volumes").then((r) => r.data);
export const createVolume = (payload) => client.post("/block-storage/volumes", payload).then((r) => r.data);
export const deleteVolume = (id) => client.delete(`/block-storage/volumes/${id}`).then((r) => r.data);

export const listProjects = () => client.get("/identity/projects").then((r) => r.data);
export const listUsers = () => client.get("/identity/users").then((r) => r.data);

export const listContainers = () => client.get("/object-storage/containers").then((r) => r.data);
export const listObjects = (container) => client.get(`/object-storage/containers/${container}/objects`).then((r) => r.data);
