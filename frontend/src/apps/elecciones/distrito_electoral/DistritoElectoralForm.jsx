
import { Formik, Form } from "formik";
import FormikFileInput from "../../../components/forms/FormikFileInput";
import getAPIBase from "../../../api/BaseAPI";

export default function DistritoElectoralForm() {

  const { crear } =getAPIBase("distrito-electoral")

  const handleSubmit = async (values, { setSubmitting }) => {
    const formData = new FormData();
    formData.append("documento", values.documento);

    try {
      await crear(formData);
      alert("Registro creado");
    } finally {
      setSubmitting(false);
    }
  };


  return (

    <Formik
      initialValues={{
        documento: null
      }}
      onSubmit={handleSubmit}
    >
      <Form>

        <FormikFileInput
          name="documento"
          label="Documento"
          accept=".pdf,.jpg,.png, .json"
        />

        <button type="submit">
          Guardar
        </button>

      </Form>
    </Formik>     
  );
} 
