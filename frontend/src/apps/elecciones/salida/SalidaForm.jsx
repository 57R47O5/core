
import { useModelForm } from "../../../hooks/useModelForm";
import { SalidaFields } from "./SalidaFields";

function SalidaForm() {
  const { FormFields} = useModelForm(SalidaFields
  );  

  return (
    <FormFields/>     
  );
}

SalidaForm.initialValuesDefault = {
  fecha: new Date().toISOString().substring(0, 10),
  estado: 2,
};

export default SalidaForm
