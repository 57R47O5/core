
import { Formik, Form, Field } from "formik";
import { Button, Form as RBForm } from "react-bootstrap";

const PersonaFisicaFilter = ({ onSearch, loading }) => {
  return (
    <>
      <h5 className="mb-3">Filtrar persona fisica</h5>
      <Formik
        initialValues={{
      id: "",
      nombres: "",
      apellidos: "",
        }}
        onSubmit={(values) => onSearch(values)}
      >
        {() => (
          <Form>
            <div className="row">
            <div className="col-md-3 mb-3">
              <RBForm.Label>ID</RBForm.Label>
              <Field name="id" className="form-control" />
            </div>
            <div className="col-md-3 mb-3">
              <RBForm.Label>Nombres</RBForm.Label>
              <Field name="nombres" className="form-control" />
            </div>
            <div className="col-md-3 mb-3">
              <RBForm.Label>Apellidos</RBForm.Label>
              <Field name="apellidos" className="form-control" />
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

export default PersonaFisicaFilter;
