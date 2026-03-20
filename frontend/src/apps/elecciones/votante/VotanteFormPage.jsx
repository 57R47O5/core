import BaseFormPage from "../../../components/forms/BaseFormPage";
import VotanteForm from "./VotanteForm";
import ContextGrid from "../../../components/displays/bento/ContextGrid";
import ContextTile from "../../../components/displays/bento/ContextTile";
import FormikFileInput from "../../../components/forms/FormikFileInput";
import getAPIBase from "../../../api/BaseAPI";
import { Formik, Form } from "formik";

function CargaMasiva() {
  const { crear } =getAPIBase("votante/carga-masiva")
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
          accept=".csv, .xls, .xmls"
        />    
        <button type="submit">
          Guardar
        </button> 
      </Form>
    </Formik>
  );  
}

export default function VotanteFormPage() {
  return (
      <ContextGrid
      defaultActive={"base"}
      controller="votante"
    >
      <ContextTile
          title="Base"
          tileKey="base"
        >
        <BaseFormPage
          FormComponent={VotanteForm}
          titleNew="Nuevo Votante"
          titleEdit="Editar Votante"
        />
      </ContextTile>
      <ContextTile
          title="Carga Masiva"
          tileKey="carga-masiva"
          capability={"crear"}> 
          <CargaMasiva />
      </ContextTile>
    </ContextGrid>
  );
}
