
import { useModelForm } from "../../../hooks/useModelForm";
import { TipoContactoFields } from "./TipoContactoFields";

export default function TipoContactoForm() {
  const TipoContactoModel = useModelForm(TipoContactoFields
  );  

  return TipoContactoModel
} 
