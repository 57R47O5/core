import * as Yup from "yup";
import SelectFormik from "../../../components/forms/SelectFormik";

export const ColaboradorFields = {

  persona: {
    label: "Persona",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().required("Requerido"),
    render: (props) => <SelectFormik {...props} />,
  },

  campana: {
    label: "Campana",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().required("Requerido"),
    render: (props) => <SelectFormik {...props} />,
  },

};