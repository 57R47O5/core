
import { useModelForm } from "../../../hooks/useModelForm";
import { ContactoFields } from "./ContactoFields";

export default function ContactoForm() {
  const ContactoModel = useModelForm(ContactoFields
  );  

  return ContactoModel
} 
