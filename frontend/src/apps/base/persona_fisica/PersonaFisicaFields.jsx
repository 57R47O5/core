import * as Yup from "yup";
import InputFormik from "../../../components/forms/InputFormik";
import DatePickerFormik from "../../../components/forms/DatePickerFormik";

export const personaFisicaFields = {
  id: {
    label: "ID",
    initial: "",
    form: false,
    filter: true, 
    validation: Yup.string().required("Requerido"),
    render: (props) => <InputFormik {...props} />,
  },
  
  nombres: {
    label: "Nombres",
    initial: "",
    form: true,
    filter: true, 
    validation: Yup.string().required("Requerido"),
    render: (props) => <InputFormik {...props} />,
  },
  
  apellidos: {
    label: "Apellidos",
    initial: "",
    form: true,
    filter: true, 
    validation: Yup.string().required("Requerido"),
    render: (props) => <InputFormik {...props} />,
  },
  
  fecha_nacimiento: {
    label: "Fecha nacimiento",
    initial: null,
    form: true,
    filter: false,
    validation: Yup.string().nullable(),
    render: (props) => <DatePickerFormik {...props} />,
  }
};
