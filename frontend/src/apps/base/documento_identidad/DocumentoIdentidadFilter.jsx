
import { Formik, Form, Field } from "formik";
import { Button, Form as RBForm } from "react-bootstrap";

const DocumentoIdentidadFilter = ({ onSearch, loading }) => {
  return (
    <>
      <h5 className="mb-3">Filtrar documento identidad</h5>

      <Formik
        initialValues={{
      persona: "",      tipo: "",      numero: "",      pais_emision: "",      vigente: "",
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
              <RBForm.Label>Tipo</RBForm.Label>
              <Field as="select" name="tipo" className="form-control">
                <option value="">Seleccione...</option>
              </Field>
            </div>
          
            <div className="col-md-3 mb-3">
              <RBForm.Label>Numero</RBForm.Label>
              <Field name="numero" className="form-control" />
            </div>
          
            <div className="col-md-3 mb-3">
              <RBForm.Label>Pais emision</RBForm.Label>
              <Field name="pais_emision" className="form-control" />
            </div>
          
            <div className="col-md-3 mb-3">
              <RBForm.Label>Vigente</RBForm.Label>
              <Field name="vigente" className="form-control" />
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

export default DocumentoIdentidadFilter;
