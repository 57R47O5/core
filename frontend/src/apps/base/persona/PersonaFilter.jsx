
import { Formik, Form, Field } from "formik";
import { Button, Form as RBForm } from "react-bootstrap";

const PersonaFilter = ({ onSearch, loading }) => {
  return (
    <>
      <h5 className="mb-3">Filtrar persona</h5>

      <Formik
        initialValues={{

        }}
        onSubmit={(values) => onSearch(values)}
      >
        {() => (
          <Form>
            <div className="row">



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

export default PersonaFilter;
