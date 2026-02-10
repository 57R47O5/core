import * as Yup from "yup";
import InputFormik from "../../../components/forms/InputFormik";
import SelectFormik from "../../../components/forms/SelectFormik";

export const SalidaFields = {

  campana: {
    label: "Campana",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().required("Requerido"),
    render: (props) => <SelectFormik {...props} />,
  },

  colaborador: {
    label: "Colaborador",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().required("Requerido"),
    render: (props) => <SelectFormik {...props} />,
  },

  fecha: {
    label: "Fecha",
    initial: "",
    form: true, 
    filter: true,
    validation: Yup.string().required("Requerido"),
    render: (props) => <InputFormik {...props} />,
  },

  estado: {
    label: "Estado",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().required("Requerido"),
    render: (props) => <SelectFormik {...props} />,
  },

};