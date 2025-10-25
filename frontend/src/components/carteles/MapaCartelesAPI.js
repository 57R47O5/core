import request from "../../api/requests";

// 🔹 Obtener lista de carteles desde el backend
export const obtenerCarteles = async () => {
  try {
    const response = await request.get("carteles/");
    return response.data || [];
  } catch (error) {
    console.error("Error al obtener carteles:", error);
    throw error;
  }
};

// 🔹 Buscar dirección en Nominatim (OpenStreetMap)
export const buscarDireccion = async (busqueda) => {
  if (!busqueda.trim()) return null;

  const url = "https://nominatim.openstreetmap.org/search";

  try {
    const response = await request.get(url, {
      params: { q: busqueda, format: "json", limit: 1 },
    });

    if (response.data.length > 0) {
      const { lat, lon } = response.data[0];
      return [parseFloat(lat), parseFloat(lon)];
    }

    return null;
  } catch (error) {
    console.error("Error al buscar dirección:", error);
    throw error;
  }
};
