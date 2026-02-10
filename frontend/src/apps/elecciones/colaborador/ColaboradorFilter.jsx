
import { Formik, Form } from "formik";
import { Button } from "react-bootstrap";
import { useModelForm } from "../../../hooks/useModelForm";
import { ColaboradorFields } from "./ColaboradorFields";

const ColaboradorFilter = ({ onSearch, loading }) => {
  const { initialValuesFilter, FilterFields } = useModelForm(
  ColaboradorFields)
  
  return (
    <>
      <h5 className="mb-3">Filtrar colaborador</h5>

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

export default ColaboradorFilter;
