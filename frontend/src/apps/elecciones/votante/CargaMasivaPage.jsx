import FormikFileInput from "../../../components/forms/FormikFileInput";
import getAPIBase from "../../../api/BaseAPI";
import { Formik, Form } from "formik";
import { Button, Spinner } from "react-bootstrap";
import CenteredCard from "../../../components/displays/CenteredCard";

export default function CargaMasivaVotantes() {
  const { crear } = getAPIBase("votante/carga-masiva");

  const handleSubmit = async (values, { setSubmitting }) => {
    const formData = new FormData();
    formData.append("documento", values.documento);

    try {
      await crear(formData);
      alert("Carga Masiva exitosa");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <CenteredCard title="Carga Masiva de Votantes">
    <Formik
      initialValues={{ documento: null }}
      onSubmit={handleSubmit}
    >
      {({ isSubmitting }) => (
        <Form>
        <div className="mb-3">
          <FormikFileInput
            name="documento"
            label="Documento"
            accept=".csv, .xls, .xlsx"
          />
        </div>
        <div className="text-end">
          <Button type="submit" variant="primary" disabled={isSubmitting}>
            {isSubmitting ? (
              <>
                <Spinner
                  as="span"
                  animation="border"
                  size="sm"
                  role="status"
                  aria-hidden="true"
                />{" "}
                Guardando...
              </>
            ) : (
                "Guardar"
            )}
          </Button>
        </div>
        </Form>
      )}
    </Formik>
    </CenteredCard>
  );
}
