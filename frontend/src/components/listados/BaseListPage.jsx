import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Spinner, Card, Table, Button } from "react-bootstrap";
import CenteredCard from "../displays/CenteredCard";
import getAPIBase from "../../api/BaseAPI";

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
export default function BaseListPage({
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

      // acceso directo si solo hay un resultado
      if (data && data.length === 1) {
        navigate(`/${controller}/${data[0].id}`);
      }
    } catch (error) {
      console.error("Error al buscar:", error);
      alert("Hubo un error al cargar los datos");
    }
    setLoading(false);
  };

  // Carga inicial sin filtros
  useEffect(() => {
    handleSearch();
  }, []);

  return (
    <div className="container">
      <h2 className="mb-4">{title}</h2>

      {/* ---------- FILTROS ---------- */}
      <CenteredCard>
        <Card.Body>
          <FilterComponent onSearch={handleSearch} loading={loading} />
        </Card.Body>
      </CenteredCard>

      {/* ---------- LISTADO ---------- */}
      <CenteredCard>
        <Card.Body>
          <h5 className="mb-3">Resultados</h5>

          {loading ? (
            <div className="text-center my-4">
              <Spinner animation="border" />
            </div>
          ) : items.length === 0 ? (
            <p className="text-center my-4">No se encontraron resultados</p>
          ) : (
            <Table striped bordered hover>
              <thead>
                <tr>
                  {columns.map((col) => (
                    <th key={col.field}>{col.label}</th>
                  ))}
                  <th>Acciones</th>
                </tr>
              </thead>

              <tbody>
                {items.map((item) => (
                  <tr key={item.id}>
                    {columns.map((col) => (
                      <td key={col.field}>{item[col.field] || "-"}</td>
                    ))}

                    <td>
                      <Button
                        size="sm"
                        onClick={() => navigate(`/${controller}/${item.id}`)}
                      >
                        Editar
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          )}
        </Card.Body>
      </CenteredCard>
    </div>
  );
}
