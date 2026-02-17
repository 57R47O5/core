import * as Yup from "yup";
import SelectFormik from "../../../components/forms/SelectFormik";

export const LugarDistritoFields = {

  distrito: {
    label: "Distrito",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().required("Requerido"),
    render: (props) => <SelectFormik {...props} />,
  },

  lugar: {
    label: "Lugar",
    initial: null,
    form: true, 
    filter: true,
    validation: Yup.number().required("Requerido"),
    render: (props) => <SelectFormik {...props} />,
  },

};