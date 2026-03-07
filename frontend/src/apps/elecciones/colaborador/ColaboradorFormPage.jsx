import BaseFormPage from "../../../components/forms/BaseFormPage";
import { useRouteMode } from "../../../hooks/useRouteMode";
import ColaboradorForm from "./ColaboradorForm";
import ContextGrid from "../../../components/displays/bento/ContextGrid";
import ContextTile from "../../../components/displays/bento/ContextTile";
import { useInstance, InstanceProvider } from "../../../context/InstanceContext";
import { DataTable, ORCTableColumna } from "../../../components/listados/DataTable";

function Colaboradores({}){
  const { instance } = useInstance();

  console.log("instance?.salida: ", instance?.salida)
  return <ContextGrid
        defaultActive={0}
        columns={2}
      >
        <ContextTile
          title="Datos Colaborador"
        >
          <BaseFormPage
            controller={"colaborador"}
            FormComponent={ColaboradorForm}
            titleNew="Nuevo Colaborador"
            titleEdit="Editar Colaborador"      
            />
        </ContextTile>        
        {instance?.salida ? <ContextTile
        title="Salidas"> 
        <DataTable
          items = {instance.salida}
          columns = {[
            {label: "Salida",  field: "salida", tipo:ORCTableColumna.LINK},
            {label: "Fecha",  field: "fecha", tipo:ORCTableColumna.FECHA},
            {label: "Estado",  field: "estado_salida", tipo:ORCTableColumna.CADENA}
          ]}
        />         
      </ContextTile>:[]}
      </ContextGrid>
}

export default function ColaboradorFormPage() {
  const {id} = useRouteMode();
  const controller = "colaborador"
  return (
    <InstanceProvider
      controller={controller} 
      id = {id}     
    >
      <Colaboradores/>
      </InstanceProvider>
  );
}
