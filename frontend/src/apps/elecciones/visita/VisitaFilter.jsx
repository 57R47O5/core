
import { Formik, Form } from "formik";
import { Button } from "react-bootstrap";
import { useModelForm } from "../../../hooks/useModelForm";
import { VisitaFields } from "./VisitaFields";

const VisitaFilter = ({ onSearch, loading }) => {
  const { initialValuesFilter, FilterFields } = useModelForm(
  VisitaFields)
  
  return (
    <>
      <h5 className="mb-3">Filtrar visita</h5>

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

export default VisitaFilter;
