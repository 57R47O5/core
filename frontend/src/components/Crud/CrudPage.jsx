import { Formik, Form } from "formik";
import { Button, Table, Spinner } from "react-bootstrap";
import useCrudState from "../../hooks/useCrudeState";

export default function CrudPage({
  title,
  api,
  initialValues,
  validationSchema,
  form,
  columns,
}) {
  const crud = useCrudState(api);

  // cargar listado inicial
  useEffect(() => {
    crud.list();
  }, []);

  if (crud.loading)
    return <div className="text-center mt-5"><Spinner animation="border" /></div>;

  return (
    <div className="container mt-4">
      <h2>{title}</h2>

      {/* ---------------------- MODO LISTADO ----------------------- */}
      {crud.mode === "list" && (
        <>
          <div className="d-flex justify-content-end mb-2">
            <Button onClick={() => crud.setMode("form-new")}>Nuevo</Button>
          </div>

          <Table striped bordered hover>
            <thead>
              <tr>
                {columns.map((c) => (
                  <th key={c.key}>{c.label}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {crud.items.map((row) => (
                <tr
                  key={row.id}
                  style={{ cursor: "pointer" }}
                  onClick={() => crud.load(row.id)}
                >
                  {columns.map((c) => (
                    <td key={c.key}>{row[c.key]}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </Table>
        </>
      )}

      {/* ---------------------- MODO FORMULARIO ----------------------- */}
      {(crud.mode === "form-new" || crud.mode === "form-edit") && (
        <Formik
          initialValues={crud.item || initialValues}
          validationSchema={validationSchema}
          onSubmit={(values) => {
            if (crud.mode === "form-new") crud.create(values);
            else crud.update(crud.item.id, values);
          }}
          enableReinitialize
        >
          {(formik) => (
            <Form className="mt-4">
              {form(formik)}

              <div className="d-flex gap-2 mt-3">
                <Button type="submit">Guardar</Button>

                <Button
                  variant="secondary"
                  onClick={() => crud.setMode("list")}
                >
                  Cancelar
                </Button>

                {crud.mode === "form-edit" && (
                  <Button
                    variant="danger"
                    onClick={() => crud.remove(crud.item.id)}
                  >
                    Eliminar
                  </Button>
                )}
              </div>
            </Form>
          )}
        </Formik>
      )}
    </div>
  );
}
