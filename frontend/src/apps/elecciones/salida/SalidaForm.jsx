
import { useModelForm } from "../../../hooks/useModelForm";
import { SalidaFields } from "./SalidaFields";

export default function SalidaForm() {
  const {FormFields} = useModelForm(SalidaFields
  );  

  return (
    <FormFields/>     
  );
} 
