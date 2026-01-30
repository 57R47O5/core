
import { Button } from "react-bootstrap";
import { Formik } from "formik";
import { useO2M } from "./O2MProvider";

export default function O2MNewRow() {
  const {
  columns,
  initialItem,
  validationSchema,
  crear,
} = useO2M();

  return (
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
              {col.render({
                formik,
                isNew: true,
              })}
            </td>
          ))}

          <td className="text-end">
            <Button
              size="sm"
              onClick={formik.handleSubmit}
            >
              +
            </Button>
          </td>
        </tr>
      )}
    </Formik>
  );
}