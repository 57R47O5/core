import { useMap } from "react-leaflet";
import { useEffect } from "react";

export default function FixMapSize() {
  const map = useMap();

  useEffect(() => {
    setTimeout(() => {
      map.invalidateSize();
    }, 200);
  }, [map]);

  return null;
}