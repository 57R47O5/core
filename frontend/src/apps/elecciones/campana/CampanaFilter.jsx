
import { Formik, Form } from "formik";
import { Button } from "react-bootstrap";
import { useModelForm } from "../../../hooks/useModelForm";
import { CampanaFields } from "./CampanaFields";

const CampanaFilter = ({ onSearch, loading }) => {
  const { initialValuesFilter, FilterFields } = useModelForm(
  CampanaFields)
  
  return (
    <>
      <h5 className="mb-3">Filtrar campana</h5>

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

export default CampanaFilter;
