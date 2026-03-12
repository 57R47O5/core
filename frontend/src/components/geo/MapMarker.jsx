import { Marker } from "react-leaflet";
import L from "leaflet";

const customMarkerIcon = L.divIcon({
  className: "custom-marker",
  iconSize: [28, 28],
  iconAnchor: [14, 28]
});

export default function MapMarker({ position }) {
  return (
    <Marker
      position={position}
      icon={customMarkerIcon}
    />
  );
}