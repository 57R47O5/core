import * as Yup from "yup";
import { PersonaFisicaFields } from "../../base/persona_fisica/PersonaFisicaFields";
import SelectFormik from "../../../components/forms/SelectFormik";
import InputFormik from "../../../components/forms/InputFormik";


export const VotanteFields = {

  ...PersonaFisicaFields,

  documento: {
    label: "Documento",
    initial: null,
    form: false,
    filter: true,
    render: (props) => <InputFormik {...props} 
      endpoint={"distrito-electoral"}/>,

  },

  distrito: {
    label: "Distrito",
    initial: null,
    form: true, 
    filter: false,
    validation: Yup.number().required("Requerido"),
    render: (props) => <SelectFormik {...props} 
      endpoint={"distrito-electoral"}/>,
  },

  seccional: {
    label: "Seccional",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().nullable(),
    render: (props) => <SelectFormik {...props} 
      endpoint={"seccional"}/>,
  },

};