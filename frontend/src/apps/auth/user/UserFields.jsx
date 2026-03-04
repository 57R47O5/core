import * as Yup from "yup";
import InputFormik from "../../../components/forms/InputFormik";
import SwitchFormik from "../../../components/forms/SwitchFormik";
import DatePickerFormik from "../../../components/forms/DatePickerFormik";

export const UserFields = {
  id: {
    label: "ID",
    initial: "",
    form: false,
    filter: true, 
    validation: Yup.string().required("Requerido"),
    render: (props) => <InputFormik {...props} />,
  },
  
  username: {
    label: "Username",
    initial: "",
    form: true,
    filter: true, 
    validation: Yup.string().required("Requerido"),
    disabled: true,
    render: (props) => <InputFormik {...props} />,
  },

  is_active: {
    label: "Activo",
    initial: "",
    form: true,
    filter: true, 
    validation: Yup.string(),
    render: (props) => <SwitchFormik {...props} />,
  }, 
created_at: {
    label: "Fecha creacion",
    initial: (new Date()).toISOString().substring(0, 10),
    form: true,
    filter: false,
    validation: Yup.string().nullable(),
    render: (props) => <DatePickerFormik {...props} />,
  }
};
