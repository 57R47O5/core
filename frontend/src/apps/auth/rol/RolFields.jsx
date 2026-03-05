import * as Yup from "yup";
import SelectFormik from "../../../components/forms/SelectFormik";

export const RolFields = {

  nombre: {
    label: "Nombre",
    initial: "",
    form: true, 
    filter: true,
    validation: Yup.string().required("Requerido"),
    render: (props) => <SelectFormik {...props} 
    endpoint={"rol"}/>,
  }

};