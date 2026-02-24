
import { useModelForm } from "../../../hooks/useModelForm";
import { VotanteFields } from "./VotanteFields";

export default function VotanteForm() {
  const {FormFields} = useModelForm(VotanteFields
  );  

  return (
    <FormFields/>     
  );
} 
