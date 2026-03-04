import { useModelForm } from "../../../hooks/useModelForm";
import { UserFields } from "./UserFields";

export default function UserForm() {
  const {FormFields} = useModelForm(UserFields);  

  return (
    <FormFields/>     
  );
} 
