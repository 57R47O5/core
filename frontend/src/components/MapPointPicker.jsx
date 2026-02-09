import { MapContainer, TileLayer, Marker, useMapEvents } from "react-leaflet";
import L from "leaflet";

function ClickHandler({ onChange }) {
  useMapEvents({
    click(e) {
      onChange({
        lat: e.latlng.lat,
        lon: e.latlng.lng,
      });
    },
  });
  return null;
}

export default function MapPointPicker({
  value,
  points = [],
  onChange,
  readOnly = false,
}) {
  return (
    <MapContainer
      center={value ? [value.lat, value.lon] : [-25.3, -57.6]} // PY default
      zoom={13}
      style={{ height: "300px", width: "100%" }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {!readOnly && <ClickHandler onChange={onChange} />}

      {value && (
        <Marker position={[value.lat, value.lon]} />
      )}

      {points.map(p => (
        <Marker key={p.id} position={[p.lat, p.lon]} />
      ))}
    </MapContainer>
  );
}
