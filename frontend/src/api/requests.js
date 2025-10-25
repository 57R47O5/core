import axios from "axios";

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
  baseURL: "http://localhost:8000/api/",
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
    // Captura de errores con mensaje personalizado
    if (error.response) {
      const { status, data } = error.response;
      const mensaje = data?.mensaje || "Error en la solicitud.";
      console.error(`Error ${status}: ${mensaje}`);
      throw new Error(mensaje);
    } else if (error.request) {
      console.error("No se recibió respuesta del servidor.");
      throw new Error("No se recibió respuesta del servidor.");
    } else {
      console.error("Error en la configuración de la solicitud:", error.message);
      throw new Error("Error en la configuración de la solicitud.");
    }
  }
);

export default request;
