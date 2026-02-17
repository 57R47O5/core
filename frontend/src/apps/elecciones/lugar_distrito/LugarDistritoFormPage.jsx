import BaseFormPage from "../../../components/forms/BaseFormPage";
import LugarDistritoForm from "./LugarDistritoForm";

export default function LugarDistritoFormPage() {
  return (
    <BaseFormPage
      controller="lugar-distrito"
      FormComponent={LugarDistritoForm}
      titleNew="Nuevo LugarDistrito"
      titleEdit="Editar LugarDistrito"
    />
  );
}
