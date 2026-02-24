import * as Yup from "yup";
import { PersonaFisicaFields } from "../../base/persona_fisica/PersonaFisicaFields";
import InputFormik from "../../../components/forms/InputFormik";
import SelectFormik from "../../../components/forms/SelectFormik";


export const VotanteFields = {

  ...PersonaFisicaFields,

  distrito: {
    label: "Distrito",
    initial: null,
    form: true, 
    filter: false,
    validation: Yup.number().required("Requerido"),
    render: (props) => <SelectFormik {...props} 
      endpoint={"distrito-electoral/options"}/>,
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