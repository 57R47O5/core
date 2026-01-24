
import { Formik, Form, Field } from "formik";
import { Button, Form as RBForm } from "react-bootstrap";

const PersonaJuridicaFilter = ({ onSearch, loading }) => {
  return (
    <>
      <h5 className="mb-3">Filtrar persona juridica</h5>

      <Formik
        initialValues={{
      persona: "",      razon_social: "",      nombre_fantasia: "",
        }}
        onSubmit={(values) => onSearch(values)}
      >
        {() => (
          <Form>
            <div className="row">


            <div className="col-md-3 mb-3">
              <RBForm.Label>Persona</RBForm.Label>
              <Field name="persona" className="form-control" />
            </div>
          
            <div className="col-md-3 mb-3">
              <RBForm.Label>Razon social</RBForm.Label>
              <Field name="razon_social" className="form-control" />
            </div>
          
            <div className="col-md-3 mb-3">
              <RBForm.Label>Nombre fantasia</RBForm.Label>
              <Field name="nombre_fantasia" className="form-control" />
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

export default PersonaJuridicaFilter;
