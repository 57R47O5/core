
import { useModelForm } from "../../../hooks/useModelForm";
import { VotanteFields } from "./VotanteFields";

export default function VotanteForm() {
  const VotanteForm = useModelForm(VotanteFields
  );  

  return VotanteForm
} 
