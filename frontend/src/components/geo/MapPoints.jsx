import { CircleMarker, Popup, useMap } from "react-leaflet";
import { useEffect } from "react";
import L from "leaflet";

export default function MapPoints({
  data = [],
  latField = "latitud",
  lngField = "longitud",
  color = "#cc0000",
  radius = 6,
  getColor,
  getLabel,
  fit = true
}) {

  const map = useMap();

  useEffect(() => {
    if (!fit || data.length === 0) return;

    const bounds = [];

    data.forEach(row => {
      const lat = row[latField];
      const lng = row[lngField];

      if (lat != null && lng != null) {
        bounds.push([lat, lng]);
      }
    });

    if (bounds.length > 0) {
      map.fitBounds(bounds, { padding: [40, 40] });
    }

  }, [data, map, fit, latField, lngField]);

  return (
    <>
      {data.map((row, i) => {

        const lat = row[latField];
        const lng = row[lngField];

        if (lat == null || lng == null) return null;

        const pointColor = getColor ? getColor(row) : color;
        const label = getLabel ? getLabel(row) : null;

        return (
          <CircleMarker
            key={i}
            center={[lat, lng]}
            radius={radius}
            pathOptions={{
              color: pointColor,
              fillColor: pointColor,
              fillOpacity: 0.9
            }}
          >
            {label && <Popup>{label}</Popup>}
          </CircleMarker>
        );
      })}
    </>
  );
}