import * as Yup from "yup";
import InputFormik from "../../../components/forms/InputFormik";

export const MonedaFields = {

  nombre: {
    label: "Nombre",
    initial: "",
    form: true, 
    filter: true,
    validation: Yup.string().required("Requerido"),
    render: (props) => <InputFormik {...props} />,
  },

  descripcion: {
    label: "Descripcion",
    initial: "",
    form: true, 
    filter: true,
    validation: Yup.string().nullable(),
    render: (props) => <InputFormik {...props} />,
  },

  simbolo: {
    label: "Simbolo",
    initial: "",
    form: true, 
    filter: true,
    validation: Yup.string().required("Requerido"),
    render: (props) => <InputFormik {...props} />,
  },

};