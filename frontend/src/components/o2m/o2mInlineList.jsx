import { useState, useEffect } from "react";
import { Spinner, Table, Button, Form } from "react-bootstrap";
import { Formik } from "formik";
import getAPIBase from "../../api/BaseAPI";

export default function O2MInlineList({
  title,
  columns,
  filtros,
  initialItem,
  validationSchema,
  controller,
}) {
    
  const { editar, crear, eliminar, buscar } = getAPIBase(controller);
  const [items, setItems] = useState({});
  const [cargando, setCargando] = useState(true);

  useEffect(()=>{
    const cargarFilas = async () => {
        const data = await buscar(filtros);
        setItems(data)
        setCargando(false)
    };

    cargarFilas();

  },[filtros])

  if (cargando) {
    return (
      <div className="text-center mt-5">
        <Spinner animation="border" />
      </div>
    );
  }

  return (
    <>
      <h5 className="mt-4">{title}</h5>

      <Table bordered size="sm">
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col.field}>{col.label}</th>
            ))}
            <th />
          </tr>
        </thead>

        <tbody>
          {/* ---------- FILAS EXISTENTES ---------- */}
          {items.map((item) => (
            <Formik
            initialValues={item}
            validationSchema={validationSchema}
            onSubmit={async (values) => {
              await editar(item.id, values);
            }}
          >
            {(formik) => (
              <tr>
                {columns.map((col) => (
                  <td key={col.field}>
                    <Form.Control
                      name={col.field}
                      value={formik.values[col.field] ?? ""}
                      onChange={formik.handleChange}
                      isInvalid={
                        formik.touched[col.field] && formik.errors[col.field]
                      }
                    />
                    <Form.Control.Feedback type="invalid">
                      {formik.errors[col.field]}
                    </Form.Control.Feedback>
                  </td>
                ))}

                <td className="text-end">
                  <Button
                    size="sm"
                    onClick={formik.handleSubmit}
                  >
                    Guardar
                  </Button>{" "}
                  <Button
                    size="sm"
                    variant="danger"
                    onClick={() => eliminar(item.id)}
                  >
                    ✕
                  </Button>
                </td>
              </tr>
            )}
          </Formik>
          ))}

          {/* ---------- FILA NUEVA ---------- */}
          <Formik
          initialValues={initialItem}
          validationSchema={validationSchema}
          onSubmit={async (values, helpers) => {
            await crear(values);
            helpers.resetForm();
          }}
        >
          {(formik) => (
            <tr>
              {columns.map((col) => (
                <td key={col.field}>
                  <Form.Control
                    name={col.field}
                    value={formik.values[col.field] ?? ""}
                    onChange={formik.handleChange}
                    isInvalid={
                      formik.touched[col.field] && formik.errors[col.field]
                    }
                  />
                </td>
              ))}

              <td className="text-end">
                <Button size="sm" onClick={formik.handleSubmit}>
                  +
                </Button>
              </td>
            </tr>
          )}
        </Formik>
        </tbody>
      </Table>
    </>
  );
}
