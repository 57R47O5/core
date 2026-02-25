
import { useModelForm } from "../../../hooks/useModelForm";
import { VisitaFields } from "./VisitaFields";

export default function VisitaForm() {
  const {FormFields} = useModelForm(VisitaFields
  );  

  return null
  return (
    <FormFields/>     
  );
} 
