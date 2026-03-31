import BaseFormPage from "../../../components/forms/BaseFormPage";
import CampanaForm from "./CampanaForm";
import ContextGrid from "../../../components/displays/bento/ContextGrid";
import ContextTile from "../../../components/displays/bento/ContextTile";

export default function CampanaFormPage() {

  return (
      <ContextGrid
        controller={"campana"}
        defaultActive={"datos-campana"}
        >
      <ContextTile
        title={"Datos Campaña"}
        tileKey={"datos-campana"}
      >
        <BaseFormPage
          FormComponent={CampanaForm}
        />
      </ContextTile>
    </ContextGrid>);
}
