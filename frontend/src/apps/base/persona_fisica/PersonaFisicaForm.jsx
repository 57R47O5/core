
import { useModelForm } from "../../../hooks/useModelForm";
import { PersonaFisicaFields } from "./PersonaFisicaFields";

export default function PersonaFisicaForm() {
  const {FormFields} = useModelForm(PersonaFisicaFields);  

  return (
    <FormFields/>     
  );
} 
