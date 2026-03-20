
import { useModelForm } from "../../../hooks/useModelForm";
import { ContactoFields } from "./ContactoFields";
import { useInstance } from "../../../context/InstanceContext";
import O2MInlineList from "../../../components/o2m/O2MInlineList";
import O2MProvider from "../../../components/o2m/O2MProvider";
import { Spinner } from "react-bootstrap";

export function ContactoPersona({}) {
  const { instance } = useInstance();

  const {
    initialValues,
    validationSchema,
    columns,
  } = useModelForm(ContactoFields);

  if (!instance)
    return (<Spinner/>)
  return (
    <O2MProvider
      controller="contacto"
      columns={columns}
      initialItem={{
        ...initialValues,
        persona: instance.persona_id, 
      }}
      validationSchema={validationSchema}
    >
      <O2MInlineList        
        filtros={{persona: instance.persona_id }}
      />
    </O2MProvider>
  );
}

export default function ContactoForm() {
  const ContactoModel = useModelForm(ContactoFields
  );  

  return ContactoModel
} 
