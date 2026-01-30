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
    buscar: async (filtros = {}) => {
    const params = new URLSearchParams();

    if (filtros && typeof filtros === "object") {
        Object.entries(filtros).forEach(([key, value]) => {
        if (value === null || value === undefined) return;

        // strings vacíos no se envían
        if (typeof value === "string" && value.trim() === "") return;

        params.append(key, value);
        });
    }

    const query = params.toString();
    const url = query ? `${controller}/?${query}` : `${controller}/`;

    return await request.get(url);
    },
})

export default getAPIBase;