import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import getAPIBase from "../../api/BaseAPI";
import { BaseListLayout } from "./BaseListLayout";
import MapPoints from "../geo/MapPoints";
import AppMap from "../geo/AppMap";

/**
 * BaseListPage
 *
 * Props:
 * - controller: string ("pacientes")
 * - FilterComponent: componente que recibe { onSearch, loading }
 *        → puede ser un Formik o un form manual
 *
 * - columns: [{ label, field }]  (para renderizar la tabla)
 * - title: título principal
 */
export default function MapListPage({
  controller,
  FilterComponent,
  columns,
  title = "Listado",
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
const position = [51.505, -0.09]
  return (
    <BaseListLayout
      title={title}
      FilterComponent={FilterComponent}
      onSearch={handleSearch}
      loading={loading}
    >
      <AppMap  center={position} zoom={13}>
        <MapPoints data={items}/>
      </AppMap>
    </BaseListLayout>
  );
}

