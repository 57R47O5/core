import request from "./requests";

const getAPIBase = (controller)=>({
    listar: async () => {
        return await request.get(controller);
    },

    // Obtener una instancia por ID
    obtener: async (id) => {
        return await request.get(`${controller}/${id}/`);
    },

    // Crear una instancia
    crear: async (datos) => {
        return await request.post(`${controller}/`, datos);
    },

    // Editar una instancia existente
    editar: async (id, datos) => {
        return await request.put(`${controller}/${id}/`, datos);
    },

    // Eliminar instancia
    eliminar: async (id) => {
        return await request.delete(`${controller}/${id}/`);
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

    return await request.get(`${controller}/?${params.toString()}`);
  },
})

export default getAPIBase;