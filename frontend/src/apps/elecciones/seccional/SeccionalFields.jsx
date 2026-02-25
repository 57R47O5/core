import * as Yup from "yup";
import SelectFormik from "../../../components/forms/SelectFormik";

export const SeccionalFields = {

  zona: {
    label: "Zona",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().required("Requerido"),
    render: (props) => <SelectFormik {...props} 
    endpoint={"lugar"}/>,
  },

  campana: {
    label: "Campana",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().required("Requerido"),
    render: (props) => <SelectFormik {...props} 
    endpoint={"campana"}/>,
  },

};