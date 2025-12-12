import { Formik, Form, Field } from "formik";
import { Button, Form as RBForm } from "react-bootstrap";

const PacientesFilter = ({ onSearch, loading }) => {
  return (
    <>
      <h5 className="mb-3">Filtrar pacientes</h5>

      <Formik
        initialValues={{
          nombre: "",
          apellido: "",
          dni: "",
          fecha_desde: "",
          fecha_hasta: "",
        }}
        onSubmit={(values) => onSearch(values)}
      >
        {() => (
          <Form>
            <div className="row">

              <div className="col-md-3 mb-3">
                <RBForm.Label>Nombre</RBForm.Label>
                <Field name="nombre" className="form-control" />
              </div>

              <div className="col-md-3 mb-3">
                <RBForm.Label>Apellido</RBForm.Label>
                <Field name="apellido" className="form-control" />
              </div>

              <div className="col-md-2 mb-3">
                <RBForm.Label>DNI</RBForm.Label>
                <Field name="dni" className="form-control" />
              </div>

              <div className="col-md-2 mb-3">
                <RBForm.Label>Desde</RBForm.Label>
                <Field name="fecha_desde" type="date" className="form-control" />
              </div>

              <div className="col-md-2 mb-3">
                <RBForm.Label>Hasta</RBForm.Label>
                <Field name="fecha_hasta" type="date" className="form-control" />
              </div>
            </div>

            <div className="text-end">
              <Button type="submit" variant="primary" disabled={loading}>
                Buscar
              </Button>
            </div>
          </Form>
        )}
      </Formik>
    </>
  );
};

export default PacientesFilter;
