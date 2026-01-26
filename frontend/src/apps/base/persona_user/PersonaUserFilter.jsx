
import { Formik, Form, Field } from "formik";
import { Button, Form as RBForm } from "react-bootstrap";

const PersonaUserFilter = ({ onSearch, loading }) => {
  return (
    <>
      <h5 className="mb-3">Filtrar persona user</h5>

      <Formik
        initialValues={{
      persona: "",      user: "",      principal: "",
        }}
        onSubmit={(values) => onSearch(values)}
      >
        {() => (
          <Form>
            <div className="row">


            <div className="col-md-3 mb-3">
              <RBForm.Label>Persona</RBForm.Label>
              <Field as="select" name="persona" className="form-control">
                <option value="">Seleccione...</option>
              </Field>
            </div>
          
            <div className="col-md-3 mb-3">
              <RBForm.Label>User</RBForm.Label>
              <Field as="select" name="user" className="form-control">
                <option value="">Seleccione...</option>
              </Field>
            </div>
          
            <div className="col-md-3 mb-3">
              <RBForm.Label>Principal</RBForm.Label>
              <Field name="principal" className="form-control" />
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

export default PersonaUserFilter;
