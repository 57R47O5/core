import request from "./requests";

const BASEURL = "personas/";

/**
 * Lista todas las personas (solo para vistas de administración o debug)
 */
export async function listPersonas() {
  try {
    const response = await request.get(BASEURL);
    return response;
  } catch (error) {
    console.error("Error listando personas:", error);
    throw error;
  }
}

/**
 * Obtiene una persona por su ID
 */
export async function getPersona(id) {
  try {
    const response = await request.get(`${BASEURL}${id}/`);
    return response;
  } catch (error) {
    console.warn("No se encontró la persona:", error);
    return null;
  }
}

/**
 * Crea una nueva persona asociada al usuario autenticado
 */
export async function createPersona(data) {
  try {
    const response = await request.post(BASEURL, data);
    return response;
  } catch (error) {
    console.error("Error creando persona:", error);
    throw error;
  }
}

/**
 * Actualiza los datos de una persona existente
 */
export async function updatePersona(id, data) {
  try {
    const response = await request.put(`${BASEURL}${id}/`, data);
    return response;
  } catch (error) {
    console.error("Error actualizando persona:", error);
    throw error;
  }
}

/**
 * Elimina una persona existente
 */
export async function deletePersona(id) {
  try {
    const response = await request.delete(`${BASEURL}${id}/`);
    return response.status === 204;
  } catch (error) {
    console.error("Error eliminando persona:", error);
    throw error;
  }
}
