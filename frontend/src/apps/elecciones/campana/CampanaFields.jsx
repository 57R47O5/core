import * as Yup from "yup";
import InputFormik from "../../../components/forms/InputFormik";
import SelectFormik from "../../../components/forms/SelectFormik";
import DatePickerFormik from "../../../components/forms/DatePickerFormik";


export const CampanaFields = {

candidato: {
  label: "Candidato",
  initial: null,
  form: true,
  filter: true,
  validation: Yup.number().required("Requerido"),
  endpoint: "persona-fisica",
  disabled: false,
  render: (props) => <SelectFormik {...props} />,
},

  cargo: {
    label: "Cargo",
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
    endpoint: "distrito-electoral/options",
    disabled: false,
    render: (props) => <SelectFormik {...props} />,
  },

  ciclo: {
    label: "Ciclo",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().required("Requerido"),
    endpoint: "ciclo-electoral/options",
    disabled: true,
    render: (props) => <SelectFormik {...props} />,
  },

  fecha_inicio: {
    label: "Fecha inicio",
    initial: "",
    form: true, 
    filter: true,
    validation: Yup.string().nullable(),
    render: (props) => <DatePickerFormik {...props} />,
  },

  fecha_fin: {
    label: "Fecha fin",
    initial: "",
    form: true, 
    filter: true,
    validation: Yup.string().nullable(),
    render: (props) => <DatePickerFormik {...props} />,
  },

};