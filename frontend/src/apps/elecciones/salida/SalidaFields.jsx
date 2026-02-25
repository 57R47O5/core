import * as Yup from "yup";
import InputFormik from "../../../components/forms/InputFormik";
import SelectFormik from "../../../components/forms/SelectFormik";
import DatePickerFormik from "../../../components/forms/DatePickerFormik";

export const SalidaFields = {

  campana: {
    label: "Campana",
    initial: null,
    form: true, 
    filter: false,
    validation: Yup.number().required("Requerido"),
    disabled:true,
    render: (props) => <SelectFormik {...props} 
      endpoint={"campana"}/>,
  },

  colaborador: {
    label: "Colaborador",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().required("Requerido"),
    render: (props) => <SelectFormik {...props} 
      endpoint={"colaborador"}/>,
  },

  fecha: {
    label: "Fecha",
    initial: "",
    form: true, 
    filter: true,
    validation: Yup.string().required("Requerido"),
    render: (props) => <DatePickerFormik {...props} />,
  },

  estado: {
    label: "Estado",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().required("Requerido"),
    render: (props) => <SelectFormik {...props} 
      endpoint={"estado-salida/options"}/>,
  },

};