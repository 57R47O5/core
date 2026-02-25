
import { useModelForm } from "../../../hooks/useModelForm";
import { CicloElectoralFields } from "./CicloElectoralFields";

export default function CicloElectoralForm() {
  const {FormFields} = useModelForm(CicloElectoralFields
  );  

  return (
    <FormFields/>     
  );
} 
