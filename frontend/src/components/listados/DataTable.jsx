import { Spinner, Table, Button, Badge } from "react-bootstrap";

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
        render: (x) => x ? <a target="_blank" href={`${x.url}`}>{String(x.label)}</a> : '',
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
}) {
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
      return col.render(valor, item);
    }

    return tipo.render(valor, item, col.field);
  };

  const getStyle = (col) => {
    const tipo = getTipo(col);

    return {
      ...tipo.estilo,
      textAlign: col.align || tipo.estilo?.textAlign,
      width: col.width,
    };
  };

  return (
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
        {items.map((item) => (
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
  );
}