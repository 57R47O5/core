
import { useModelForm } from "../../../hooks/useModelForm";
import { CampanaFields } from "./CampanaFields";

export default function CampanaForm() {

  const CampanaForm = useModelForm(CampanaFields);

  return CampanaForm;
} 
