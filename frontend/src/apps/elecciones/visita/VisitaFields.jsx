import * as Yup from "yup";
import InputFormik from "../../../components/forms/InputFormik";
import SelectFormik from "../../../components/forms/SelectFormik";
import FormikGeoPoint from "../../../components/forms/FormikGeoPoint";
import FormikAutocompleteRemote from "../../../components/forms/FormikAutocompleteRemote";

export const VisitaFields = {

  salida: {
    label: "Salida",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().required("Debe seleccionar una salida en curso"),
    endpoint: "salida",
    render: (props) => <SelectFormik {...props} />,
  },

  votante: {
    label: "Votante",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().required("Debe seleccionar un votante"),
    endpoint: "votantes",
    render: (props) => <FormikAutocompleteRemote {...props} />,
  },

  lugar: {
    label: "Lugar",
    initial: null,
    form: true, 
    filter: false,
    validation: Yup.object({
      lat: Yup.number().nullable(),
      lon: Yup.number().nullable(),
    })
    .test(
      "valid-coordinates",
      "Favor marcar la ubicación",
      (value) => {
        return value?.lat != null && value?.lon != null;
      }
    ),
    endpoint: "lugar",
    mode: "ubicacion",
    render: (props) => <FormikGeoPoint {...props} />,
  },

  fecha: {
    label: "Fecha",
    initial: "",
    form: false, 
    filter: true,
    validation: Yup.string().required("La visita debe tener un resultado"),
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
    filter: false,
    validation: Yup.string().nullable(),
    endpoint: "notas",
    render: (props) => <InputFormik {...props} />,
  },

};