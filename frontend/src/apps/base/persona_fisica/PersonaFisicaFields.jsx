import * as Yup from "yup";
import InputFormik from "../../../components/forms/InputFormik";
import DatePickerFormik from "../../../components/forms/DatePickerFormik";

export const PersonaFisicaFields = {
  id: {
    label: "ID",
    initial: "",
    form: false,
    filter: true, 
    validation: Yup.string(),
    render: (props) => <InputFormik {...props} />,
  },
  
  nombres: {
    label: "Nombres",
    initial: "",
    form: true,
    filter: true, 
    validation: Yup.string().required("El nombre es requerido"),
    render: (props) => <InputFormik {...props} />,
  },
  
  apellidos: {
    label: "Apellidos",
    initial: "Perez",
    form: true,
    filter: true, 
    validation: Yup.string().required("El apellido es requerido"),
    render: (props) => <InputFormik {...props} />,
  },
  
  fecha_nacimiento: {
    label: "Fecha nacimiento",
    initial: (new Date()).toISOString().substring(0, 10),
    form: true,
    filter: false,
    validation: Yup.string().nullable(),
    render: (props) => <DatePickerFormik {...props} />,
  }
};
