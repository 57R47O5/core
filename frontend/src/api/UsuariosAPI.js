import request from "./requests";

const controller = "usuarios";

export const obtenerUsuarios = async () => {
  const response = await request.get(`${controller}/`);
  return response || [];
};

export const obtenerMedicos = async () => {
  const response = await request.get(`${controller}/`);
  return response || [];
};

export const obtenerUsuario = async (id) => {
  const response = await request.get(`${controller}/${id}/`);
  return response;
};

export const crearUsuario = async (data) => {
  const response = await request.post(`${controller}/register/`, data);
  return response;
};

export const editarUsuario = async (id, data) => {
  const response = await request.put(`${controller}/${id}/`, data);
  return response;
};
