import * as Yup from "yup";
import InputFormik from "../../../components/forms/InputFormik";
import SelectFormik from "../../../components/forms/SelectFormik";

export const LugarFields = {

  tipo: {
    label: "Tipo",
    initial: "",
    form: true, 
    filter: true,
    validation: Yup.string().required("Requerido"),
    endpoint: "tipo",
    render: (props) => <InputFormik {...props} />,
  },

  geometry_data: {
    label: "Geometry data",
    initial: "",
    form: true, 
    filter: true,
    validation: Yup.string().nullable(),
    endpoint: "geometry_data",
    render: (props) => <InputFormik {...props} />,
  },

  centroide_lat: {
    label: "Centroide lat",
    initial: "",
    form: true, 
    filter: true,
    validation: Yup.string().nullable(),
    endpoint: "centroide_lat",
    render: (props) => <InputFormik {...props} />,
  },

  centroide_lon: {
    label: "Centroide lon",
    initial: "",
    form: true, 
    filter: true,
    validation: Yup.string().nullable(),
    endpoint: "centroide_lon",
    render: (props) => <InputFormik {...props} />,
  },

  padre: {
    label: "Padre",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().nullable(),
    endpoint: "padre",
    render: (props) => <SelectFormik {...props} />,
  },

  nivel: {
    label: "Nivel",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().required("Requerido"),
    endpoint: "nivel",
    render: (props) => <SelectFormik {...props} />,
  },

  activo: {
    label: "Activo",
    initial: "",
    form: true, 
    filter: true,
    validation: Yup.string().required("Requerido"),
    endpoint: "activo",
    render: (props) => <InputFormik {...props} />,
  },

  created_at: {
    label: "Created at",
    initial: "",
    form: true, 
    filter: true,
    validation: Yup.string().required("Requerido"),
    endpoint: "created_at",
    render: (props) => <InputFormik {...props} />,
  },

  updated_at: {
    label: "Updated at",
    initial: "",
    form: true, 
    filter: true,
    validation: Yup.string().required("Requerido"),
    endpoint: "updated_at",
    render: (props) => <InputFormik {...props} />,
  },

};