import { Formik, Form } from "formik";
import { useModelForm } from "../../hooks/useModelForm";
import ABMFilterActions from "./ABMFilterActions";

const ABMFilter = ({
  title,
  fields,
  controller,
  onSearch,
  loading = false
}) => {
  const { initialValuesFilter, FilterFields } = useModelForm(fields);

  return (
    <>
      {title && <h5 className="mb-3">{title}</h5>}

      <Formik
        initialValues={initialValuesFilter}
        onSubmit={onSearch}
      >
        <Form>
          <div className="row">
            <FilterFields />
          </div>

          <ABMFilterActions
            controller={controller}
            loading={loading}
          />
        </Form>
      </Formik>
    </>
  );
};

export default ABMFilter;