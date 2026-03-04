
import { useModelForm } from "../../../hooks/useModelForm";
import { RolFields } from "./RolFields";

export default function RolForm() {
  const {FormFields} = useModelForm(RolFields
  );  

  return (
    <FormFields/>     
  );
} 
