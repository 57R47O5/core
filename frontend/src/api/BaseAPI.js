import request from "./requests";
import { alertarExito } from "../utils/alertas";

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
      const res = await request.post(`${controller}/`, datos);
      alertarExito(res, "Creación exitosa");
      return res;
    },


    // Editar una instancia existente
    editar: async (id, datos) => {
      const res = await request.put(`${controller}/${id}/`, datos);
      alertarExito(res, "Edición exitosa");
      return res;
    },

    // Eliminar instancia
    eliminar: async (id) => {
      const res = await request.delete(`${controller}/${id}/`);
      alertarExito(res, "Eliminación exitosa");
      return res;
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