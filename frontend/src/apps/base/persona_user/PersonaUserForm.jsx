
import { Formik, Form } from "formik";
import * as Yup from "yup";
import { Button } from "react-bootstrap";
import InputFormik from "../../../components/forms/InputFormik";
import SelectFormik from "../../../components/forms/SelectFormik";

export const PersonaUserSchema = Yup.object().shape({
  persona: Yup.mixed().nullable(),  user: Yup.mixed().nullable(),  principal: Yup.mixed().nullable(),
});

export function PersonaUserFormFields({ prefix = "" }) {
  const fieldName = (name) => prefix ? `${prefix}.${name}` : name;

  return (
    <>
    
      <SelectFormik
        name="persona"
        label="Persona"
        endpoint="persona"
      />
          
      <SelectFormik
        name="user"
        label="User"
        endpoint="user"
      />
          
      <InputFormik
        name="principal"
        label="Principal"
      />
          
    </>
  );
}

export default function PersonaUserForm({
  initialValues,
  onSubmit,
  submitText = "Guardar",
  submitting = false,
}) {
  return (
    <Formik
      enableReinitialize
      initialValues={initialValues}
      validationSchema={PersonaUserSchema}
      onSubmit={onSubmit}
    >
      {({ errors, touched }) => (
        <Form>

      <SelectFormik
        name="persona"
        label="Persona"
        endpoint="persona"
      />
          
      <SelectFormik
        name="user"
        label="User"
        endpoint="user"
      />
          
      <InputFormik
        name="principal"
        label="Principal"
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
