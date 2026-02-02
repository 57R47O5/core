
import { Button } from "react-bootstrap";
import { Formik } from "formik";
import { useO2M } from "./O2MProvider";

export default function O2MNewRow() {
  const {
  columns,
  initialItem,
  validationSchema,
  crear,
  refresh
} = useO2M();

  return (
    <Formik
      initialValues={initialItem}
      validationSchema={validationSchema}
      onSubmit={async (values, helpers, setSubmitting) => {
        try {
          await crear(values);
          refresh();
        } finally {
          setSubmitting(false);
          helpers.resetForm();
        }
      }}
    >
      {(formik) => (
        <tr>
          {columns.map((col) => (
            <td key={col.field}>
              {col.render({
                formik,
                isNew: true,
              })}
            </td>
          ))}

          <td className="text-end">
            <Button
              size="sm"
              disabled={formik.isSubmitting}
              onClick={formik.handleSubmit}
            >
              Agregar
            </Button>
          </td>
        </tr>
      )}
    </Formik>
  );
}