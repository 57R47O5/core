import { useRouteMode } from "../../../hooks/useRouteMode";
import BaseFormPage from "../../../components/forms/BaseFormPage";
import VotanteForm from "./VotanteForm";
import ContextGrid from "../../../components/displays/bento/ContextGrid";
import ContextTile from "../../../components/displays/bento/ContextTile";
import { DocumentosPersona } from "../../base/documento_identidad/DocumentoIdentidadForm";
import { ContactoPersona } from "../../base/contacto/ContactoForm";

export default function VotanteFormPage() {
  const { isEdit } = useRouteMode();
  return (
      <ContextGrid
      defaultActive={"base"}
      controller="votante"
    >
      <ContextTile
          title="Base"
          tileKey="base"
        >
        <BaseFormPage
          FormComponent={VotanteForm}
          titleNew="Nuevo Votante"
          titleEdit="Editar Votante"
        />
      </ContextTile>
        <ContextTile
          title = "Documentos"
          tileKey = "documentos"
        >
        {isEdit && (<DocumentosPersona/>)}
        </ContextTile> 
        <ContextTile
          title = "Informacion de Contacto"
          tileKey = "contactos"
        >
        {isEdit && (<ContactoPersona/>)}
        </ContextTile>
    </ContextGrid>
  );
}
