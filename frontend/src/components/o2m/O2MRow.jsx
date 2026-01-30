
import { Button } from "react-bootstrap";
import { Formik } from "formik";
import { useO2M } from "./O2MProvider";

export default function O2MRow({item}) {
  const { columns, editar, eliminar, validationSchema } = useO2M();
  return (
    <Formik
      initialValues={item}
      validationSchema={validationSchema}
      onSubmit={(values) => editar(item.id, values)}
    >
      {(formik) => (
        <tr>
          {columns.map(col => (
            <td key={col.field}>
              {col.render({ formik, item })}
            </td>
          ))}
          <td className="text-end">
            <Button size="sm" onClick={formik.handleSubmit}>Guardar</Button>
            <Button size="sm" variant="danger" onClick={() => eliminar(item.id)}>
              ✕
            </Button>
          </td>
        </tr>
      )}
    </Formik>
  );
}
