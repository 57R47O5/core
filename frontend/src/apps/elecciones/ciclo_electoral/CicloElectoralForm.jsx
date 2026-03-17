
import { useModelForm } from "../../../hooks/useModelForm";
import { CicloElectoralFields } from "./CicloElectoralFields";

export default function CicloElectoralForm() {
  const CicloElectoralForm = useModelForm(CicloElectoralFields
  );  

  return CicloElectoralForm;
} 
