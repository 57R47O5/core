
import { useModelForm } from "../../../hooks/useModelForm";
import { ColaboradorFields } from "./ColaboradorFields";

export default function ColaboradorForm() {
  const {FormFields} = useModelForm(ColaboradorFields
  );  

  return (
    <FormFields/>     
  );
} 
