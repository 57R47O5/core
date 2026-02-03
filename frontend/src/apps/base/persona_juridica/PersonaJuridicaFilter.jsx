
import { Formik, Form } from "formik";
import { Button } from "react-bootstrap";
import { PersonaJuridicaFields } from "./PersonaJuridicaFields";
import { useModelForm } from "../../../hooks/useModelForm";

const PersonaJuridicaFilter = ({ onSearch, loading }) => {

  const {initialValuesFilter, FilterFields} = useModelForm(PersonaJuridicaFields)

  return (
    <>
      <h5 className="mb-3">Filtrar persona juridica</h5>

      <Formik
        initialValues={initialValuesFilter}
        onSubmit={(values) => onSearch(values)}
      >
        {() => (
          <Form>
            <div className="row">
            <FilterFields/>
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