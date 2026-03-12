import { useEffect } from "react";
import { useMap, MapContainer, TileLayer } from "react-leaflet";
import "./../forms/map.css"

export function FixMapSize() {
  const map = useMap();

  useEffect(() => {
      // invalidar tamaño apenas se monta
    requestAnimationFrame(() => {
      map.invalidateSize();
      console.log("InvalidateSize con RAF");
      console.log("Container size:", map.getContainer().offsetWidth, map.getContainer().offsetHeight);
      console.log("Map size:", map.getSize());
    });

      const container = map.getContainer();
      const resize = () => map.invalidateSize();
      window.addEventListener("resize", resize);

      return () => window.removeEventListener("resize", resize);
    }, [map]);

  return null;
}

export default function AppMap({ center, zoom = 13, children }) {
  return (
    <MapContainer center={center} zoom={zoom} 
    className="form-map-container">
      <FixMapSize />
      <TileLayer
        attribution="© OpenStreetMap"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {children}
    </MapContainer>
  );
}