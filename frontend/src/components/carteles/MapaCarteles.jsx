import React, { useState, useEffect } from "react";
import MapaUbicacion from "./MapaUbicacion";
import { Marker, Popup, useMap } from "react-leaflet";
import L from "leaflet";
import axios from "axios";

const iconoCartel = new L.Icon({
  iconUrl: "https://cdn-icons-png.flaticon.com/512/684/684908.png",
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

const MapaCarteles = ({ onUbicacionSeleccionada }) => {
  const [carteles, setCarteles] = useState([]);
  const [busqueda, setBusqueda] = useState("");
  const [posicionMapa, setPosicionMapa] = useState([-25.2637, -57.5759]); // Ejemplo: Asunción

  // 🔹 Cargar carteles desde la API
  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/carteles/")
      .then((res) => setCarteles(res.data))
      .catch((err) => console.error("Error al obtener carteles:", err));
  }, []);

  // 🔹 Buscar dirección en Nominatim (OpenStreetMap)
  const handleBuscar = async () => {
    if (!busqueda.trim()) return;
    try {
      const response = await axios.get("https://nominatim.openstreetmap.org/search", {
        params: { q: busqueda, format: "json", limit: 1 },
      });
      if (response.data.length > 0) {
        const { lat, lon } = response.data[0];
        setPosicionMapa([parseFloat(lat), parseFloat(lon)]);
      } else {
        alert("No se encontró la dirección.");
      }
    } catch (err) {
      console.error("Error al buscar dirección:", err);
    }
  };

  // 🔹 Componente auxiliar para mover el mapa al buscar
  const MoverMapa = ({ posicion }) => {
    const map = useMap();
    useEffect(() => {
      map.setView(posicion, 14);
    }, [posicion, map]);
    return null;
  };

  return (
    <div>
      {/* Barra de búsqueda */}
      <div style={{ marginBottom: "8px", display: "flex", gap: "4px" }}>
        <input
          type="text"
          placeholder="Buscar dirección..."
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
          style={{ flex: 1, padding: "8px" }}
        />
        <button onClick={handleBuscar}>Buscar</button>
      </div>

      {/* Reutilizamos el mapa base */}
      <MapaUbicacion
        latitudInicial={posicionMapa[0]}
        longitudInicial={posicionMapa[1]}
        onUbicacionChange={onUbicacionSeleccionada}
      >
        {/* Este contenido se inyecta dentro del mapa */}
        <MoverMapa posicion={posicionMapa} />

        {/* Marcadores de carteles existentes */}
        {carteles.map((cartel) => (
          <Marker
            key={cartel.id}
            position={[cartel.latitud, cartel.longitud]}
            icon={iconoCartel}
          >
            <Popup>
              <strong>{cartel.tipo_cartel?.nombre || "Cartel"}</strong><br />
              {cartel.direccion || "Sin dirección"}<br />
              {cartel.precio_exhibicion
                ? `Precio: ${cartel.precio_exhibicion} Gs`
                : "Precio no disponible"}
            </Popup>
          </Marker>
        ))}
      </MapaUbicacion>
    </div>
  );
};

export default MapaCarteles;
