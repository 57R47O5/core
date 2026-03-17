
import { useModelForm } from "../../../hooks/useModelForm";
import { PersonaJuridicaFields } from "./PersonaJuridicaFields";

export default function PersonaJuridicaForm() {
  const personaJuridicaModel = useModelForm(PersonaJuridicaFields
  );  

  return personaJuridicaModel
} 
