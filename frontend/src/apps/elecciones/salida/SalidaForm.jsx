
import { useModelForm } from "../../../hooks/useModelForm";
import { SalidaFields } from "./SalidaFields";

function SalidaForm() {
  const { FormFields} = useModelForm(SalidaFields
  );  

  return (
    <FormFields/>     
  );
}

export default SalidaForm
