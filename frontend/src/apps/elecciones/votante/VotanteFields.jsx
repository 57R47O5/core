import * as Yup from "yup";
import InputFormik from "../../../components/forms/InputFormik";
import SelectFormik from "../../../components/forms/SelectFormik";

export const VotanteFields = {

  persona: {
    label: "Persona",
    initial: "",
    form: true, 
    filter: true,
    validation: Yup.string().required("Requerido"),
    render: (props) => <InputFormik {...props} />,
  },

  distrito: {
    label: "Distrito",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().required("Requerido"),
    render: (props) => <SelectFormik {...props} />,
  },

  seccional: {
    label: "Seccional",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().nullable(),
    render: (props) => <SelectFormik {...props} />,
  },

};