import { Formik, Form } from "formik";
import { Button } from "react-bootstrap";
import { personaFisicaFields } from "./PersonaFisicaFields";
import { useModelForm } from "../../../hooks/useModelForm";

const PersonaFisicaFilter = ({ onSearch, loading }) => {
  const {initialValuesFilter, FilterFields } = useModelForm(
    personaFisicaFields)

  return (
    <>
      <h5 className="mb-3">Filtrar persona fisica</h5>
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

export default PersonaFisicaFilter;
