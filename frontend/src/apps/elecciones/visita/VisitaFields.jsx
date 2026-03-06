import * as Yup from "yup";
import InputFormik from "../../../components/forms/InputFormik";
import SelectFormik from "../../../components/forms/SelectFormik";

export const VisitaFields = {

  salida: {
    label: "Salida",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().required("Requerido"),
    endpoint: "salida",
    render: (props) => <SelectFormik {...props} />,
  },

  votante: {
    label: "Votante",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().required("Requerido"),
    endpoint: "votante",
    render: (props) => <SelectFormik {...props} />,
  },

  lugar: {
    label: "Lugar",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().required("Requerido"),
    endpoint: "lugar",
    render: (props) => <SelectFormik {...props} />,
  },

  fecha: {
    label: "Fecha",
    initial: "",
    form: true, 
    filter: true,
    validation: Yup.string().required("Requerido"),
    endpoint: "fecha",
    render: (props) => <InputFormik {...props} />,
  },

  resultado: {
    label: "Resultado",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().required("Requerido"),
    endpoint: "resultado-visita/options",
    render: (props) => <SelectFormik {...props} />,
  },

  notas: {
    label: "Notas",
    initial: "",
    form: true, 
    filter: true,
    validation: Yup.string().nullable(),
    endpoint: "notas",
    render: (props) => <InputFormik {...props} />,
  },

};