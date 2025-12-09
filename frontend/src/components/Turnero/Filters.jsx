import React from "react";
import { Formik, Form, Field } from "formik";
import { Button, Form as RBForm } from "react-bootstrap";
import * as Yup from "yup";

const schema = Yup.object().shape({
  tipo: Yup.string().required(),
  fecha_inicio: Yup.string().required("La fecha es obligatoria")
});

const Filters = ({ filtros, setFiltros }) => {
  return (
    <Formik
      initialValues={filtros}
      validationSchema={schema}
      onSubmit={(values) => setFiltros(values)}
    >
      {({ errors, touched }) => (
        <Form>
          <RBForm.Group className="mb-3">
            <RBForm.Label>Tipo de vista</RBForm.Label>
            <Field as="select" name="tipo" className="form-select">
              <option value="diario">Diario</option>
              <option value="semanal">Semanal</option>
              <option value="mensual">Mensual</option>
            </Field>
          </RBForm.Group>

          <RBForm.Group className="mb-3">
            <RBForm.Label>Fecha</RBForm.Label>
            <Field type="date" name="fecha_inicio" className="form-control" />
            {errors.fecha_inicio && touched.fecha_inicio && (
              <div className="text-danger">{errors.fecha_inicio}</div>
            )}
          </RBForm.Group>

          <RBForm.Group className="mb-3">
            <RBForm.Label>Odontólogo</RBForm.Label>
            <Field as="select" name="odontologo" className="form-select">
              <option value="">Todos</option>
              {/* map de odontologos */}
            </Field>
          </RBForm.Group>

          <RBForm.Group className="mb-3">
            <RBForm.Label>Paciente</RBForm.Label>
            <Field as="select" name="paciente" className="form-select">
              <option value="">Todos</option>
              {/* map de pacientes */}
            </Field>
          </RBForm.Group>

          <Button type="submit" variant="primary" className="w-100">
            Aplicar filtros
          </Button>
        </Form>
      )}
    </Formik>
  );
};

export default Filters;
