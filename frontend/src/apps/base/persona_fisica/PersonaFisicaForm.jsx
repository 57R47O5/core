
import { Formik, Form } from "formik";
import * as Yup from "yup";
import { Button } from "react-bootstrap";
import InputFormik from "../../../components/forms/InputFormik";
import DatePickerFormik from "../../../components/forms/DatePickerFormik";
import {DocumentoIdentidadFormFields, DocumentoIdentidadSchema} from "../documento_identidad/DocumentoIdentidadForm";
import { useRouteMode } from "../../../hooks/useRouteMode";

export const PersonaFisicaSchema = Yup.object().shape({
  nombres: Yup.string().required(),
  apellidos: Yup.string().required(),
  fecha_nacimiento: Yup.string().nullable(),
  ...DocumentoIdentidadSchema,
  });
  
export function PersonaFisicaFormFields() {
  const {isCreate} = useRouteMode()
  return (
    <>               
      <InputFormik
        name="nombres"
        label="Nombres"
      />          
      <InputFormik
        name="apellidos"
        label="Apellidos"
      />         
      <DatePickerFormik
        name="fecha_nacimiento"
        label="Fecha nacimiento"
      />
      {isCreate && <DocumentoIdentidadFormFields/>}   
    </>
  );
}

export default function PersonaFisicaForm({
  initialValues,
  onSubmit,
  submitText = "Guardar",
  submitting = false,
}) {
  return (
    <Formik
      enableReinitialize
      initialValues={initialValues}
      validationSchema={PersonaFisicaSchema}
      onSubmit={onSubmit}
    >
      {(formik) => (
        <Form>
     <PersonaFisicaFormFields/>          
          <div className="text-end mt-3">
            <Button type="submit" disabled={submitting}>
              {submitting ? "Guardando..." : submitText}
            </Button>
          </div>

        </Form>
      )}
    </Formik>
  );
} 
