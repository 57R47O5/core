import { Spinner, Table, Button } from "react-bootstrap";

export function DataTable({ items, columns, onEdit, loading }) {
  if (loading) {
    return (
      <div className="text-center my-4">
        <Spinner animation="border" />
      </div>
    );
  }

  if (items.length === 0) {
    return <p className="text-center my-4">No se encontraron resultados</p>;
  }

  return (
    <Table striped bordered hover>
      <thead>
        <tr>
          {columns.map(col => (
            <th key={col.field}>{col.label}</th>
          ))}
          <th>Acciones</th>
        </tr>
      </thead>

      <tbody>
        {items.map(item => (
          <tr key={item.id}>
            {columns.map(col => (
              <td key={col.field}>{item[col.field] ?? "-"}</td>
            ))}
            <td>
              <Button size="sm" onClick={() => onEdit(item)}>
                Editar
              </Button>
            </td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
}
