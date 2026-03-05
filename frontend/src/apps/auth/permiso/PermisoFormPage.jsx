import BaseFormPage from "../../../components/forms/BaseFormPage";
import PermisoForm from "./PermisoForm";

export default function PermisoFormPage() {
  return (
    <BaseFormPage
      controller="permiso"
      FormComponent={PermisoForm}
      titleNew="Nuevo Permiso"
      titleEdit="Editar Permiso"
    />
  );
}
