import request from "../../api/requests"; 

const BASE_URL = "turnos/";

  // Obtener lista completa (no usar para autocomplete)
export const listar = async () => {
    return await request.get(BASE_URL);
  };

  // Obtener un turno por ID
export const obtener = async (id) => {
    return await request.get(`${BASE_URL}${id}/`);
  };

  // Crear un turno
export const crear = async (datos) => {
    return await request.post(`${BASE_URL}nuevo/`, datos);
  };

  // Editar un paciente existente
export const editar = async (id, datos) => {
    return await request.put(`${BASE_URL}${id}/`, datos);
  };

  // Eliminar paciente
export const eliminar = async (id) => {
    return await request.delete(`${BASE_URL}${id}/`);
  };

  // Búsqueda / Autocomplete
export const   buscar= async (texto) => {
    if (!texto || texto.trim() === "") return [];

    return await request.get(`${BASE_URL}buscar/?q=${encodeURIComponent(texto)}`);
  };

export const diarios = async (fecha, odontologo = "") => {
    const params = new URLSearchParams({ fecha });
    if (odontologo) params.append("odontologo", odontologo);
    
    return await request.get(`${BASE_URL}diario/?${params.toString()}`);
  };
  
  export const getTurnos = async (filtros) => {
    const params = new URLSearchParams(filtros).toString();
    
  return await request.get(`${BASE_URL}?${params.toString()}`);
  
};