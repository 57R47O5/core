import * as Yup from "yup";
import InputFormik from "../../../components/forms/InputFormik";
import SelectFormik from "../../../components/forms/SelectFormik";

export const documentoIdentidadFields = {
  persona_id: {
    label: "Persona",
    initial: "",
    validation: Yup.number().required("Requerido"),
    render: (props) => (
      <InputFormik
        {...props}
        endpoint="tipo-documento-identidad"
        disabled
      />
    ),
  },

  tipo: {
    label: "Tipo Documento",
    initial: "",
    validation: Yup.number().required("Requerido"),
    render: (props) => (
      <SelectFormik
        {...props}
        endpoint="tipo-documento-identidad"
      />
    ),
  },

  numero: {
    label: "Número de documento",
    initial: "",
    validation: Yup.string().required("Requerido"),
    render: (props) => (
      <InputFormik {...props} />
    ),
  },
};
