import axios from "axios";
import { Alertar, Tipo } from "../utils/alertas";

// --- Función auxiliar para obtener el CSRF token ---
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// --- Crear instancia principal de axios ---
const request = axios.create({
  baseURL: "http://localhost:8000/",
  withCredentials: true,
});

// --- Interceptor para agregar CSRF token a todas las peticiones ---
request.interceptors.request.use((config) => {
  const token = getCookie("csrftoken");
  if (token) {
    config.headers["X-CSRFToken"] = token;
  }
  return config;
});

// --- Interceptor para manejar respuestas y errores ---
request.interceptors.response.use(
  (response) => {
    // Si la respuesta es exitosa (2xx)
    return response.data;
  },
  (error) => {
    let mensaje = "Error inesperado en el servidor.";

    if (error.response) {
      const data = error.response.data;

      if (data && data.mensaje) {
        mensaje = data.mensaje;
      } 
      else {
        mensaje = "Error al procesar la solicitud.";
      }
    } 
    else if (error.request) {
      mensaje = "El servidor no respondió.";
    } 
    else {
      mensaje = "Error al preparar la solicitud.";
    }

    Alertar(mensaje, Tipo.ERROR, "Error");

    throw new Error(mensaje);
  }
);

export default request;
