
import { Button } from "react-bootstrap";
import { Formik } from "formik";
import { useO2M } from "./O2MProvider";

export default function O2MRow({item}) {
  const { columns, editar, eliminar, validationSchema, refresh } = useO2M();
  return (
    <Formik
      initialValues={item}
      validationSchema={validationSchema}
      onSubmit={async (values, { setSubmitting }) => {
        try {
          await editar(item.id, values);
          refresh(); 
        } finally {
          setSubmitting(false);
        }
      }}
    >
      {(formik) => (
        <tr>
          {columns.map(col => (
            <td key={col.field}>
              {col.render({ formik, item })}
            </td>
          ))}
          <td className="text-end">
            <div className="col-12 col-lg-2 d-flex align-items-center justify-content-center mt-3">
              <Button
                size="sm"
                disabled={formik.isSubmitting}
                onClick={formik.handleSubmit}
                >
                Guardar
              </Button>
              <Button
                size="sm"
                variant="danger"
                disabled={formik.isSubmitting}
                onClick={async () => {
                  if (!confirm("¿Eliminar este registro?")) return;
                  
                  await eliminar(item.id);
                  refresh();
                }}
                >
                Eliminar
              </Button>
            </div>
          </td>
        </tr>
      )}
    </Formik>
  );
}
