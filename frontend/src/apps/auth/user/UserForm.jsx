import { useModelForm } from "../../../hooks/useModelForm";
import { UserFields } from "./UserFields";

export default function UserForm() {
  const UserForm = useModelForm(UserFields);  

  return UserForm
} 
