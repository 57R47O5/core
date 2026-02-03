import * as Yup from "yup";
import InputFormik from "../../../components/forms/InputFormik";

export const PersonaJuridicaFields = {
  id: {
    label: "ID",
    initial: "",
    form: false,
    filter: true, 
    validation: Yup.string(),
    render: (props) => <InputFormik {...props} />,
  },  

  razon_social: {
    label: "Razón Social",
    initial: "",
    form: true,
    filter: true, 
    validation: Yup.string().required("Requerido"),
    render: (props) => <InputFormik {...props} />,
  },  

  nombre_fantasia: {
    label: "Nombre Fantasía",
    initial: "",
    form: true,
    filter: true, 
    validation: Yup.string(),
    render: (props) => <InputFormik {...props} />,
  }
};
