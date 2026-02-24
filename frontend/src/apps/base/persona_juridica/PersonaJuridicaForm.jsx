
import { useModelForm } from "../../../hooks/useModelForm";
import { PersonaJuridicaFields } from "./PersonaJuridicaFields";

export default function PersonaJuridicaForm() {
  const {FormFields} = useModelForm(PersonaJuridicaFields
  );  

  return (
    <FormFields/>     
  );
} 
