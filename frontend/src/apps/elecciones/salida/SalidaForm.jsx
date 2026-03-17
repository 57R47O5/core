
import { useModelForm } from "../../../hooks/useModelForm";
import { SalidaFields } from "./SalidaFields";

export default function SalidaForm() {
  const SalidaForm = useModelForm(SalidaFields
  );  

  return SalidaForm
}

