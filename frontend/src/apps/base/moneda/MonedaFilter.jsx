
import { Formik, Form, Field } from "formik";
import { Button, Form as RBForm } from "react-bootstrap";

const MonedaFilter = ({ onSearch, loading }) => {
  return (
    <>
      <h5 className="mb-3">Filtrar moneda</h5>

      <Formik
        initialValues={{
      id: "",      nombre: "",      descripcion: "",      simbolo: "",
        }}
        onSubmit={(values) => onSearch(values)}
      >
        {() => (
          <Form>
            <div className="row">


            <div className="col-md-3 mb-3">
              <RBForm.Label>Id</RBForm.Label>
              <Field name="id" className="form-control" />
            </div>
          
            <div className="col-md-3 mb-3">
              <RBForm.Label>Nombre</RBForm.Label>
              <Field name="nombre" className="form-control" />
            </div>
          
            <div className="col-md-3 mb-3">
              <RBForm.Label>Descripcion</RBForm.Label>
              <Field name="descripcion" className="form-control" />
            </div>
          
            <div className="col-md-3 mb-3">
              <RBForm.Label>Simbolo</RBForm.Label>
              <Field name="simbolo" className="form-control" />
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

export default MonedaFilter;
