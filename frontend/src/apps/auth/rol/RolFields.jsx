import * as Yup from "yup";
import InputFormik from "../../../components/forms/InputFormik";

export const RolFields = {

  nombre: {
    label: "Nombre",
    initial: "",
    form: true, 
    filter: true,
    validation: Yup.string().required("Requerido"),
    endpoint: "nombre",
    render: (props) => <InputFormik {...props} />,
  },

  descripcion: {
    label: "Descripcion",
    initial: "",
    form: true, 
    filter: true,
    validation: Yup.string().nullable(),
    endpoint: "descripcion",
    render: (props) => <InputFormik {...props} />,
  },

};