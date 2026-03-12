import { GeoJSON } from "react-leaflet";

export default function MapGeoJSON({ geometry }) {

  return (
    <GeoJSON
      data={geometry}
      style={{
        color: "#0044cc",
        weight: 2,
        fillOpacity: 0.2
      }}
    />
  );
}