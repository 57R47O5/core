import './datatable.css'
import { useState } from "react";
import { Spinner, Table, Button, Badge, Pagination } from "react-bootstrap";
import BaseLink from "../displays/BaseLink";

function formatFecha(value) {
  if (!value) return "--";

  const date = new Date(value);

  return new Intl.DateTimeFormat("es-PY", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  }).format(date);
}

function formatFechaHora(value) {
  if (!value) return "--";

  const date = new Date(value);

  return new Intl.DateTimeFormat("es-PY", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}

export const ORCTableColumna = {
    ID: {
        render: (fila, campo) => String(fila[campo]),
        estilo: {},
    },
    NUMERICO: {
        render: (x) => (x ? x.toLocaleString("de-DE") : x),
        estilo: { textAlign: "right" },
    },
    LINK: {
        render: (x) => {
            if (!x) return "";

            const url = x.url.startsWith("/") ? x.url : `/${x.url}`;

            return (
                <BaseLink to={url}>
                    {x.label}
                </BaseLink>
            );
        },
        estilo: {},
    },
    LINK_CONTROLADO: {
      render: (x, item, field, col) => {
        if (!x) return "";

        const controller = col.controller || "";
        const url = `/${controller}/${x}/`;
        const display = col.fieldDisplay ? item[col.fieldDisplay] : x;

        return (
          <BaseLink to={url}>
            {display}
          </BaseLink>
        );
      },
      estilo: {},
    },
    CADENA: {
        render: (x) => (x == null ? "" : String(x)),
        estilo: {},
    },
    GUARANIES: {
        render: (x) => {
            return x ? x.toLocaleString("de-DE", { currency: "PYG" }) + " Gs." : '';
        },
        estilo: { textAlign: "right" },
    },
    DOLARES: {
        render: (x) => {
            return x.toLocaleString("en-US", { currency: "USD" }) + " $.";
        },
        estilo: { textAlign: "right" },
    },
    FECHA: {
      render: (x) => formatFecha(x),
      estilo: {},
    },

    FECHA_HORA: {
      render: (x) => formatFechaHora(x),
      estilo: {},
    },
    SINO: {
        render: (x) => (x === "S" ? "SÍ" : "NO"),
        estilo: {},
    },
    MES: {
        render: (x) => {
            if (!x) return "N/A"; 
            const MESES = {
                1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
                5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
                9: "Setiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
            };
            return MESES[Number(x)] || x;
        },
        estilo: {},
    },
    BOOLEANO: {
      render: (x) => {
        if (x === true) {
          return <Badge bg="success">Sí</Badge>;
        }
        if (x === false) {
          return <Badge bg="secondary">No</Badge>;
        }
        return "--";
      },
      estilo: { textAlign: "center" },
    },
};



export function DataTable({
  items = [],
  columns = [],
  onEdit,
  loading,
  pageSize = 5, // cantidad de filas por página
}) {
  const [currentPage, setCurrentPage] = useState(1);

  if (loading) {
    return (
      <div className="text-center my-4">
        <Spinner animation="border" />
      </div>
    );
  }

  if (!items || items.length === 0) {
    return <p className="text-center my-4">No se encontraron resultados</p>;
  }

  const getTipo = (col) => col.tipo || ORCTableColumna.CADENA;

  const renderCell = (item, col) => {
    const tipo = getTipo(col);
    const valor = item[col.field];

    if (col.render) {
      return col.render(valor, item, col);
    }

    return tipo.render(valor, item, col.field, col);
  };

  const getStyle = (col) => {
    const tipo = getTipo(col);

    return {
      ...tipo.estilo,
      textAlign: col.align || tipo.estilo?.textAlign,
      width: col.width,
    };
  };

  // --- Paginación ---
  const totalPages = Math.ceil(items.length / pageSize);
  const startIndex = (currentPage - 1) * pageSize;
  const paginatedItems = items.slice(startIndex, startIndex + pageSize);

  return (
    <div className="responsive-table">
      <Table striped bordered hover>
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col.field} style={getStyle(col)}>
                {col.label}
              </th>
            ))}
            {onEdit && <th style={{ width: "120px" }}>Acciones</th>}
          </tr>
        </thead>

        <tbody>
          {paginatedItems.map((item) => (
            <tr key={item.id}>
              {columns.map((col) => (
                <td key={col.field} style={getStyle(col)}>
                  {renderCell(item, col)}
                </td>
              ))}

              {onEdit && (
                <td>
                  <Button size="sm" onClick={() => onEdit(item)}>
                    Editar
                  </Button>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </Table>

      {/* Componente de paginación */}
      <div className="d-flex justify-content-center">
        <Pagination>
          <Pagination.First onClick={() => setCurrentPage(1)} disabled={currentPage === 1} />
          <Pagination.Prev onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))} disabled={currentPage === 1} />

          <Pagination.Item active>{currentPage}</Pagination.Item>


          <Pagination.Next
            onClick={() => setCurrentPage((p) => Math.min(p + 1, totalPages))}
            disabled={currentPage === totalPages}
          />
          <Pagination.Last onClick={() => setCurrentPage(totalPages)} disabled={currentPage === totalPages} />
        </Pagination>
      </div>
    </div>
  );
}