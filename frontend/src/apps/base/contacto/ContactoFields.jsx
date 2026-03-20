import * as Yup from "yup";
import SelectFormik from "../../../components/forms/SelectFormik";

export const ContactoFields = {

  persona: {
    label: "Persona",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().required("Requerido"),
    endpoint: "persona",
    render: (props) => <SelectFormik {...props} />,
  },

  tipo: {
    label: "Tipo",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().required("Requerido"),
    endpoint: "tipo",
    render: (props) => <SelectFormik {...props} />,
  },

};