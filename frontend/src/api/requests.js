import axios from "axios";
import { Alertar, Tipo } from "../utils/alertas";
import { getToken, clearToken } from "./tokenService";

// --- Instancia principal de axios ---
const request = axios.create({
  baseURL: "/api/",
  withCredentials: true
});

request.interceptors.request.use((config) => {
  const esFormData = (config.data instanceof FormData)
  if (!esFormData) {
    config.headers["Content-Type"] = "application/json";
  }
  return config;
});

// --- Interceptor de request (token si existe) ---
request.interceptors.request.use(
  (config) => {
    const token = getToken();

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// --- Interceptor de response ---
request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    let mensaje = "Error inesperado en el servidor.";

    if (error.response?.data) {
      const { mensaje: beMensaje, callstack } = error.response.data;

      if (beMensaje) {
        mensaje = beMensaje;
      }

      if (callstack) {
        console.error("BE callstack:", callstack);
      }
      else if (error.response?.status===401){
      clearToken();
    }
    } else if (error.request) {
      mensaje = "El servidor no respondió.";
    } else {
      mensaje = "Error al preparar la solicitud.";
    }

    Alertar(mensaje, Tipo.ERROR, "Error");

    return Promise.reject(error);
  }
);

export default request;
