import { useState, useEffect } from "react";
import MapaUbicacion from "../Mapa";
import { Marker, Popup, useMap } from "react-leaflet";
import L from "leaflet";
import { obtenerCarteles, buscarDireccion } from "./MapaCartelesAPI";
import iconoCartelImg from "../../icons/cartel.png";

const iconoCartel = new L.Icon({
  iconUrl: iconoCartelImg,
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

const MapaCarteles = () => {
  const [carteles, setCarteles] = useState([]);
  const [busqueda, setBusqueda] = useState("");
  const [posicionMapa, setPosicionMapa] = useState([-25.2637, -57.5759]);

  useEffect(() => {
    const cargarCarteles = async () => {
      try {
        const data = await obtenerCarteles();
        setCarteles(data);
      } catch {}
    };
    cargarCarteles();
  }, []);

  const handleBuscar = async () => {
    const nuevaPosicion = await buscarDireccion(busqueda);
    if (nuevaPosicion) {
      setPosicionMapa(nuevaPosicion);
    } else {
      alert("No se encontró la dirección.");
    }
  };

  const MoverMapa = ({ posicion }) => {
    const map = useMap();
    useEffect(() => {
      map.setView(posicion, 14);
    }, [posicion, map]);
    return null;
  };

  return (
    <div>
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

      <MapaUbicacion
        latitudInicial={posicionMapa[0]}
        longitudInicial={posicionMapa[1]}
        onUbicacionChange={() => {}}
      >
        <MoverMapa posicion={posicionMapa} />

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

export const MapaNuevoCartel = ({ onUbicacionSeleccionada }) => {
  const [posicion, setPosicion] = useState(null);

  const handleUbicacion = ({ lat, lng }) => {
    setPosicion([lat, lng]);
    onUbicacionSeleccionada({ lat, lng });
  };

  return (
    <MapaUbicacion
      latitudInicial={-25.2637}
      longitudInicial={-57.5759}
      onUbicacionChange={handleUbicacion}
    >
      {posicion && (
        <Marker position={posicion} icon={iconoCartel}>
          <Popup>
            Ubicación seleccionada: {posicion[0]}, {posicion[1]}
          </Popup>
        </Marker>
      )}
    </MapaUbicacion>
  );
};

