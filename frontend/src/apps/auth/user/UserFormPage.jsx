import BaseFormPage from "../../../components/forms/BaseFormPage";
import UserForm from "./UserForm";
import { Spinner, Card } from "react-bootstrap";
import O2MProvider from "../../../components/o2m/O2MProvider";
import O2MInlineList from "../../../components/o2m/O2MInlineList";
import { useInstance, InstanceProvider } from "../../../context/InstanceContext";
import ContextGrid from "../../../components/displays/bento/ContextGrid";
import ContextTile from "../../../components/displays/bento/ContextTile";
import EntityLink from "../../../components/displays/EntityLink";
import { useRouteMode } from "../../../hooks/useRouteMode";
import { useModelForm } from "../../../hooks/useModelForm";
import { UserRolFields } from "../user_rol/UserRolFields"
import { PermisoFields } from "../permiso/PermisoFields"
import CenteredCard from "../../../components/displays/CenteredCard";
import ORCTable from "../../../components/displays/table/ORCTable";

function Persona({}){
  const { instance } = useInstance();

  return  (
  <EntityLink
      controller={"persona-fisica"}
      id = {instance?.persona_fisica?.id}
      label = {instance?.persona_fisica?.nombres}      
  />)

}

function RolesUser({}) {
  const { instance } = useInstance();

  const {
    initialValues,
    validationSchema,
    columns,
  } = useModelForm(UserRolFields);

  if (!instance)
    return (<Spinner/>)
  return (
    <O2MProvider
      controller="user-rol"
      columns={columns}
      initialItem={{
        ...initialValues,
        user: instance.id, 
      }}
      validationSchema={validationSchema}
    >
      <O2MInlineList
        title="Roles"
        filtros={{"user":instance?.id}}
      />
    </O2MProvider>
  );
}

function PermisosUser({}) {
  const { instance } = useInstance();


  const {
    initialValues,
    validationSchema,
    columns,
  } = useModelForm(PermisoFields);


  if (!instance)
    return (<Spinner/>)
  return (
    <O2MProvider
      controller="rol-permiso"
      columns={columns}
      initialItem={{
        ...initialValues,
        id: instance.id, 
      }}
      validationSchema={validationSchema}
    >
      <CenteredCard title={"Permisos"}>
        <Card.Body>
          <ORCTable
            columns = {[{field: "permiso", label: "Permiso"}]}
            data={instance.permisos}
            size = "m"
            />
        </Card.Body>
      </CenteredCard>
    </O2MProvider>
  );
}

export default function UserFormPage() {
  const {id } = useRouteMode();
  const controller = "user";
  return (
    <InstanceProvider
      controller={controller} 
      id = {id}      
    >
      <ContextGrid
        defaultActive={0}
        columns={2}
        >
        <ContextTile
          title="Datos Usuario"
        >
        <BaseFormPage
          controller="user"
          FormComponent={UserForm}
          titleNew="Usuario"
          titleEdit="Usuario"
          />
        </ContextTile>
        <ContextTile
          title={"Persona"}
          > 
           <Persona/>  
        </ContextTile> 
        <ContextTile
        title={"Roles"}
        >
          <RolesUser/>
          </ContextTile>           
      </ContextGrid>
    </InstanceProvider>
  );
}
