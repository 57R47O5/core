
import { useModelForm } from "../../../hooks/useModelForm";
import { VisitaFields } from "./VisitaFields";

export default function VisitaForm() {
  const VisitaForm = useModelForm(VisitaFields
  );  

  return VisitaForm
} 
