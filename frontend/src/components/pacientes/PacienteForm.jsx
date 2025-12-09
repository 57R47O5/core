import { Formik, Form, Field } from "formik";
import * as Yup from "yup";
import { Form as RBForm, Button } from "react-bootstrap";

export const PacienteSchema = Yup.object().shape({
  nombre: Yup.string().required("El nombre es obligatorio"),
  apellido: Yup.string().required("El apellido es obligatorio"),
  dni: Yup.string().nullable(),
  telefono: Yup.string().nullable(),
  email: Yup.string().email("Email inválido").nullable(),
  notas: Yup.string().nullable(),
});

const PacienteForm = ({
  initialValues,
  onSubmit,
  submitText = "Guardar",
  submitting = false,
}) => {
  return (
    <Formik
      enableReinitialize
      initialValues={initialValues}
      validationSchema={PacienteSchema}
      onSubmit={onSubmit}
    >
      {({ errors, touched }) => (
        <Form>
          {/* Nombre */}
          <RBForm.Group className="mb-3">
            <RBForm.Label>Nombre *</RBForm.Label>
            <Field
              name="nombre"
              className={`form-control ${
                errors.nombre && touched.nombre ? "is-invalid" : ""
              }`}
            />
            {errors.nombre && touched.nombre && (
              <div className="invalid-feedback">{errors.nombre}</div>
            )}
          </RBForm.Group>

          {/* Apellido */}
          <RBForm.Group className="mb-3">
            <RBForm.Label>Apellido *</RBForm.Label>
            <Field
              name="apellido"
              className={`form-control ${
                errors.apellido && touched.apellido ? "is-invalid" : ""
              }`}
            />
            {errors.apellido && touched.apellido && (
              <div className="invalid-feedback">{errors.apellido}</div>
            )}
          </RBForm.Group>

          {/* DNI */}
          <RBForm.Group className="mb-3">
            <RBForm.Label>DNI</RBForm.Label>
            <Field name="dni" className="form-control" />
          </RBForm.Group>

          {/* Telefono */}
          <RBForm.Group className="mb-3">
            <RBForm.Label>Teléfono</RBForm.Label>
            <Field name="telefono" className="form-control" />
          </RBForm.Group>

          {/* Email */}
          <RBForm.Group className="mb-3">
            <RBForm.Label>Email</RBForm.Label>
            <Field
              name="email"
              className={`form-control ${
                errors.email && touched.email ? "is-invalid" : ""
              }`}
            />
            {errors.email && touched.email && (
              <div className="invalid-feedback">{errors.email}</div>
            )}
          </RBForm.Group>

          {/* Notas */}
          <RBForm.Group className="mb-3">
            <RBForm.Label>Notas</RBForm.Label>
            <Field
              as="textarea"
              name="notas"
              rows={3}
              className="form-control"
            />
          </RBForm.Group>

          {/* Botón */}
          <div className="text-end">
            <Button type="submit" disabled={submitting}>
              {submitting ? "Guardando..." : submitText}
            </Button>
          </div>
        </Form>
      )}
    </Formik>
  );
};

export default PacienteForm;
