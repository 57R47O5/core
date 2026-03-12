import * as Yup from "yup";
import SelectFormik from "../../../components/forms/SelectFormik";
import DatePickerFormik from "../../../components/forms/DatePickerFormik";

export const SalidaFields = {

  campana: {
    label: "Campaña",
    initial: null,
    form: true, 
    filter: false,
    validation: Yup.number().required("Requerido"),
    disabled: false,
    autoSelectSingle: true,
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
    initial: (new Date()).toISOString().substring(0, 10),
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