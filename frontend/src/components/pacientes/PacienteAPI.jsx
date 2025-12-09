import request from "../../api/requests";

const BASE_URL = "pacientes/";

const PacienteAPI = {
  // Obtener lista completa (no usar para autocomplete)
  listar: async () => {
    return await request.get(BASE_URL);
  },

  // Obtener un paciente por ID
  obtener: async (id) => {
    return await request.get(`${BASE_URL}${id}/`);
  },

  // Crear un paciente
  crear: async (datos) => {
    return await request.post(BASE_URL, datos);
  },

  // Editar un paciente existente
  editar: async (id, datos) => {
    return await request.put(`${BASE_URL}${id}/`, datos);
  },

  // Eliminar paciente
  eliminar: async (id) => {
    return await request.del(`${BASE_URL}${id}/`);
  },

  // Búsqueda / Autocomplete
  buscar: async (filtros) => {
  // Si no se envía nada, devolvemos []
  // if (!filtros || typeof filtros !== "object") return [];

  // Construir parámetros dinámicos
  const params = new URLSearchParams();

  if (filtros.nombre) params.append("nombre", filtros.nombre.trim());
  if (filtros.apellido) params.append("apellido", filtros.apellido.trim());
  if (filtros.dni) params.append("dni", filtros.dni.trim());

  if (filtros.fecha_desde) params.append("fecha_desde", filtros.fecha_desde);
  if (filtros.fecha_hasta) params.append("fecha_hasta", filtros.fecha_hasta);

  // Si no hay filtros rellenados, devolver []
  // if ([...params.entries()].length === 0) return [];

  return await request.get(`${BASE_URL}buscar/?${params.toString()}`);
  },
};

export default PacienteAPI;
