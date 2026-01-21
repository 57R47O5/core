
import { Formik, Form, Field } from "formik";
import { Button, Form as RBForm } from "react-bootstrap";

const UserRolFilter = ({ onSearch, loading }) => {
  return (
    <>
      <h5 className="mb-3">Filtrar user rol</h5>

      <Formik
        initialValues={{
      user: "",      rol: "",
        }}
        onSubmit={(values) => onSearch(values)}
      >
        {() => (
          <Form>
            <div className="row">


            <div className="col-md-3 mb-3">
              <RBForm.Label>User</RBForm.Label>
              <Field as="select" name="user" className="form-control">
                <option value="">Seleccione...</option>
              </Field>
            </div>
          
            <div className="col-md-3 mb-3">
              <RBForm.Label>Rol</RBForm.Label>
              <Field as="select" name="rol" className="form-control">
                <option value="">Seleccione...</option>
              </Field>
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

export default UserRolFilter;
