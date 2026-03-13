
import { useModelForm } from "../../../hooks/useModelForm";
import { CampanaFields } from "./CampanaFields";

export default function CampanaForm() {

  const {FormFields} = useModelForm(CampanaFields);

  return (
  <>
    <FormFields/>
  </>
  );
} 
