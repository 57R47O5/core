import axios from "axios";
import { Alertar, Tipo } from "../utils/alertas";

// --- Instancia principal de axios ---
const request = axios.create({
  baseURL: "http://localhost:8000/",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

// --- Interceptor de request (token si existe) ---
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");

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
