
import { Formik, Form } from "formik";
import * as Yup from "yup";
import { Button } from "react-bootstrap";
import SelectFormik from "../../components/formik/SelectFormik";

export const UserRolSchema = Yup.object().shape({
  user: Yup.mixed().nullable(),  rol: Yup.mixed().nullable(),
});

export function UserRolFormFields({ prefix = "" }) {
  const fieldName = (name) => prefix ? `${prefix}.${name}` : name;

  return (
    <>
    
      <SelectFormik
        name="user"
        label="User"
        endpoint="user"
      />
          
      <SelectFormik
        name="rol"
        label="Rol"
        endpoint="rol"
      />
          
    </>
  );
}

export default function UserRolForm({
  initialValues,
  onSubmit,
  submitText = "Guardar",
  submitting = false,
}) {
  return (
    <Formik
      enableReinitialize
      initialValues={initialValues}
      validationSchema={UserRolSchema}
      onSubmit={onSubmit}
    >
      {({ errors, touched }) => (
        <Form>

      <SelectFormik
        name="user"
        label="User"
        endpoint="user"
      />
          
      <SelectFormik
        name="rol"
        label="Rol"
        endpoint="rol"
      />
          
          <div className="text-end mt-3">
            <Button type="submit" disabled={submitting}>
              {submitting ? "Guardando..." : submitText}
            </Button>
          </div>

        </Form>
      )}
    </Formik>
  );
}
