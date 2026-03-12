import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import getAPIBase from "../../api/BaseAPI";
import { BaseListLayout } from "./BaseListLayout";
import MapPoints from "../geo/MapPoints";
import AppMap from "../geo/AppMap";

/**
 * MapListPage
 *
 * Props:
 * - controller: string ("pacientes")
 * - FilterComponent: componente que recibe { onSearch, loading }
 *        → puede ser un Formik o un form manual
 *
 * - columns: [{ label, field }]  (para renderizar la tabla)
 * - title: título principal
 */

function interpolateColor(value, domain, colors) {
  const [min, max] = domain;
  const ratio = (value - min) / (max - min);

  const index = ratio * (colors.length - 1);
  const low = Math.floor(index);
  const high = Math.min(low + 1, colors.length - 1);
  const mix = index - low;

  return `color-mix(in oklch,
    ${colors[low]} ${(1 - mix) * 100}%,
    ${colors[high]} ${mix * 100}%
  )`;
}

export default function MapListPage({
  controller,
  FilterComponent,
  title = "Listado",
  colorScale 
}) {
  const navigate = useNavigate();
  const { buscar } = getAPIBase(controller);

  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (filters = {}) => {
    setLoading(true);
    try {
      const data = await buscar(filters);
      setItems(data || []);

      if (data?.length === 1) {
        navigate(`/${controller}/${data[0].id}`);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handleSearch();
  }, []);

  const getColor = (row) => {
    if (!colorScale) return "#3388ff";

    const value = row[colorScale.field];

    return interpolateColor(
      value,
      colorScale.domain,
      colorScale.colors
    );
  };

  const getLabel = (row) => {
    return row.descripcion
  }

  const position = [-25.2637, -57.5759]; 

  return (
    <BaseListLayout
      title={title}
      FilterComponent={FilterComponent}
      onSearch={handleSearch}
      loading={loading}
    >
      <AppMap center={position} zoom={13}>
        <MapPoints
          data={items}
          getColor={getColor}
          getLabel={getLabel}
        />
      </AppMap>
    </BaseListLayout>
  );
}
