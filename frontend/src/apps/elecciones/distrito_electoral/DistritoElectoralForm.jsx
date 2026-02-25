
import { useModelForm } from "../../../hooks/useModelForm";
import { DistritoElectoralFields } from "./DistritoElectoralFields";

export default function DistritoElectoralForm() {
  const {FormFields} = useModelForm(DistritoElectoralFields
  );  

  return (
    <FormFields/>     
  );
} 
