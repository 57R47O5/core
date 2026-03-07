import {
  MapContainer,
  TileLayer,
  Marker,
  useMap,
  useMapEvents
} from "react-leaflet";
import { useField, useFormikContext } from "formik";
import { useState } from "react";
import FixMapSize from "./FixMapSize";
import "./map.css";

function ChangeView({ center }) {
  const map = useMap();
  map.setView(center, map.getZoom());
  return null;
}

function MapClickHandler({ name }) {
  const { setFieldValue } = useFormikContext();

  useMapEvents({
    click(e) {
      const { lat, lng } = e.latlng;

      setFieldValue(name, {
        lat,
        lon: lng
      });
    }
  });

  return null;
}

export default function FormikGeoPoint({ name }) {
  const [field] = useField(name);
  const { setFieldValue } = useFormikContext();

  const value = field.value;

  const defaultCenter = [-25.2637, -57.5759];

  const position = value
    ? [parseFloat(value.lat), parseFloat(value.lon)]
    : defaultCenter;

  const [center, setCenter] = useState(position);
  const [search, setSearch] = useState("");

  const usarUbicacionActual = () => {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const lat = pos.coords.latitude;
        const lon = pos.coords.longitude;

        setFieldValue(name, { lat, lon });
        setCenter([lat, lon]);
      },
      () => alert("No se pudo obtener ubicación"),
      { enableHighAccuracy: true }
    );
  };

  const buscarDireccion = async () => {
    if (!search) return;

    const url =
      "https://nominatim.openstreetmap.org/search?format=json&q=" +
      encodeURIComponent(search);

    const res = await fetch(url);
    const data = await res.json();

    if (data.length > 0) {
      const lat = parseFloat(data[0].lat);
      const lon = parseFloat(data[0].lon);

      setCenter([lat, lon]);
      setFieldValue(name, { lat, lon });
    }
  };

  return (
    <div className="form-map-wrapper">

      {/* buscador */}
      <div className="form-map-search">
        <input
          type="text"
          placeholder="Buscar dirección..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="form-map-input"
        />

        <button
          type="button"
          onClick={buscarDireccion}
          className="form-map-search-btn"
        >
          🔎
        </button>
      </div>

      {/* mapa */}
      <div className="form-map-container">
        <MapContainer
          center={center}
          zoom={15}
        >
          <FixMapSize />
          <ChangeView center={center} />

          <TileLayer
            attribution="© OpenStreetMap"
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          <MapClickHandler name={name} />

          {value && (
            <Marker
              draggable
              position={[
                parseFloat(value.lat),
                parseFloat(value.lon)
              ]}
              eventHandlers={{
                dragend: (e) => {
                  const p = e.target.getLatLng();

                  setFieldValue(name, {
                    lat: p.lat,
                    lon: p.lng
                  });
                }
              }}
            />
          )}
        </MapContainer>

        {/* botón GPS flotante */}
        <button
          type="button"
          onClick={usarUbicacionActual}
          className="form-map-gps-btn"
        >
          📍
        </button>
      </div>

      {/* coordenadas */}
      {value && (
        <div className="form-map-coords">
          Lat: {value.lat} | Lon: {value.lon}
        </div>
      )}
    </div>
  );
}