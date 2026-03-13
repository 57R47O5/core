import * as Yup from "yup";
import SelectFormik from "../../../components/forms/SelectFormik";
import { PersonaFisicaFields } from "../../base/persona_fisica/PersonaFisicaFields";
import { documentoIdentidadFields } from "../../base/documento_identidad/DocumentoIdentidadFields";

export const ColaboradorFields = {

  ...PersonaFisicaFields,
  ...documentoIdentidadFields,

};