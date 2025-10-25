import { useState, useEffect } from "react";
import MapaUbicacion from "../Mapa";
import { Marker, Popup, useMap } from "react-leaflet";
import L from "leaflet";
import { obtenerCarteles, buscarDireccion } from "./MapaCartelesAPI";

const iconoCartel = new L.Icon({
  iconUrl: "https://cdn-icons-png.flaticon.com/512/684/684908.png",
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

const MapaCarteles = ({ onUbicacionSeleccionada }) => {
  const [carteles, setCarteles] = useState([]);
  const [busqueda, setBusqueda] = useState("");
  const [posicionMapa, setPosicionMapa] = useState([-25.2637, -57.5759]); // Asunción

  // 🔹 Cargar carteles desde la API
  useEffect(() => {
    const cargarCarteles = async () => {
      try {
        const data = await obtenerCarteles();
        setCarteles(data);
      } catch {
        // ya se loguea el error dentro de la función API
      }
    };
    cargarCarteles();
  }, []);

  // 🔹 Buscar dirección y mover mapa
  const handleBuscar = async () => {
    const nuevaPosicion = await buscarDireccion(busqueda);
    if (nuevaPosicion) {
      setPosicionMapa(nuevaPosicion);
    } else {
      alert("No se encontró la dirección.");
    }
  };

  // 🔹 Componente auxiliar para mover el mapa
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
        <MoverMapa posicion={posicionMapa} />

        {/* Mostrar marcadores solo si hay carteles */}
        {carteles.length > 0 &&
          carteles.map((cartel) => (
            <Marker
              key={cartel.id}
              position={[cartel.latitud, cartel.longitud]}
              icon={iconoCartel}
            >
              <Popup>
                <strong>{cartel.tipo_cartel?.nombre || "Cartel"}</strong>
                <br />
                {cartel.direccion || "Sin dirección"}
                <br />
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
