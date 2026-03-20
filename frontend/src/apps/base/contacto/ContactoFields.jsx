import * as Yup from "yup";
import SelectFormik from "../../../components/forms/SelectFormik";
import InputFormik from "../../../components/forms/InputFormik";

export const ContactoFields = {

  persona: {
    label: "Persona",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().required("Requerido"),
    endpoint: "persona",
    render: (props) => (
      <InputFormik
        {...props}
        disabled
      />
    ),
  },

  tipo: {
    label: "Tipo",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().required("Requerido"),
    render: (props) => <SelectFormik {...props} 
    endpoint="tipo-contacto/options"
    />,
  },

  valor: {
    label: "Valor",
    initial: "",
    form: true,
    filter: false,
    validation: Yup.string().required("Requerido"),
    render: (props) => <InputFormik {...props} />,
  }

};