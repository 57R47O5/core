import * as Yup from "yup";
import InputFormik from "../../../components/forms/InputFormik";
import DatePickerFormik from "../../../components/forms/DatePickerFormik";
import { documentoIdentidadFields } from "../documento_identidad/DocumentoIdentidadFields";

export const personaFisicaFields = {
  nombres: {
    label: "Nombres",
    initial: "",
    validation: Yup.string().required("Requerido"),
    render: (props) => <InputFormik {...props} />,
  },

  apellidos: {
    label: "Apellidos",
    initial: "",
    validation: Yup.string().required("Requerido"),
    render: (props) => <InputFormik {...props} />,
  },

  fecha_nacimiento: {
    label: "Fecha nacimiento",
    initial: null,
    validation: Yup.string().nullable(),
    render: (props) => <DatePickerFormik {...props} />,
  },

  ...documentoIdentidadFields,
};
