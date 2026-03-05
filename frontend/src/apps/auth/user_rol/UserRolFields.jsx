import * as Yup from "yup";
import SelectFormik from "../../../components/forms/SelectFormik";

export const UserRolFields = {
  
  rol: {
    label: "Rol",
    initial: "",
    validation: Yup.number().required("Requerido"),
    render: (props) => (
      <SelectFormik 
      {...props} 
      endpoint={"rol/options"}
      />
    ),
  }

};