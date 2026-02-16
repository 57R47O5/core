import * as Yup from "yup";
import InputFormik from "../../../components/forms/InputFormik";
import SelectFormik from "../../../components/forms/SelectFormik";
import { personaFisicaFields } from "../../base/persona_fisica/PersonaFisicaFields";
import { documentoIdentidadFields } from "../../base/documento_identidad/DocumentoIdentidadFields";

export const ColaboradorFields = {

  ...personaFisicaFields,
  ...documentoIdentidadFields

};