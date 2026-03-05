
import { useModelForm } from "../../../hooks/useModelForm";
import { PermisoFields } from "./PermisoFields";

export default function PermisoForm() {
  const {FormFields} = useModelForm(PermisoFields
  );  

  return (
    <FormFields/>     
  );
} 
