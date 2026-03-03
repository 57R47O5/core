import * as Yup from "yup";
import SelectFormik from "../../../components/forms/SelectFormik";
import { PersonaFisicaFields } from "../../base/persona_fisica/PersonaFisicaFields";
import { documentoIdentidadFields } from "../../base/documento_identidad/DocumentoIdentidadFields";

export const ColaboradorFields = {

  ...PersonaFisicaFields,
  ...documentoIdentidadFields,
    user: {
      label: "Usuario",
      initial: "",
      form: true,
      filter: true, 
      validation: Yup.string().required("Requerido"),
      endpoint: "/colaborador/usuarios-disponibles",
      disabled: false,
      render: (props) => <SelectFormik {...props} />,
    },

};