import BaseFormPage from "../../../components/forms/BaseFormPage";
import { useRouteMode } from "../../../hooks/useRouteMode";
import ColaboradorForm from "./ColaboradorForm";
import { InstanceProvider } from "../../../context/InstanceContext";

export default function ColaboradorFormPage() {
  const {id} = useRouteMode();
  const controller = "colaborador"
  return (
    <InstanceProvider
      controller={controller} 
      id = {id}     
    >
      <BaseFormPage
        controller={controller}
        FormComponent={ColaboradorForm}
        titleNew="Nuevo Colaborador"
        titleEdit="Editar Colaborador"      
        />
      </InstanceProvider>
  );
}
