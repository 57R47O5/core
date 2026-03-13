import BaseFormPage from "../../../components/forms/BaseFormPage";
import { useRouteMode } from "../../../hooks/useRouteMode";
import ColaboradorForm from "./ColaboradorForm";
import ContextGrid from "../../../components/displays/bento/ContextGrid";
import ContextTile from "../../../components/displays/bento/ContextTile";
import { useInstance, InstanceProvider } from "../../../context/InstanceContext";
import { DataTable, ORCTableColumna } from "../../../components/listados/DataTable";
import VisitaList from "../visita/VisitaList";
import SelectFormik from "../../../components/forms/SelectFormik";
import { Form, Formik } from "formik";
import getAPIBase from "../../../api/BaseAPI";
import { Button } from "react-bootstrap";
import { SiTiene } from "../../../components/displays/SiTiene";
import EntityLink from "../../../components/displays/EntityLink";

function User({ instance }){

  const { crear } = getAPIBase("persona-user");

  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      await crear(values);
      alert("Registro creado");
    } finally {
      setSubmitting(false);
    }
  };
  if (instance.user==null)
  return (<Formik
          initialValues={{persona: instance.persona, user: null}}
          onSubmit={handleSubmit}>
            {(formik) => (
              <Form>
                <SelectFormik
                  name="user"
                  label="Usuario"
                  endpoint={"/colaborador/usuarios-disponibles"}
                />
                {!formik.isSubmitting && (
                  <SiTiene capacidad={"crear_usuario"}>
                    <Button type="submit" variant="primary">
                      Enviar
                    </Button>
                  </SiTiene>
                )}
              </Form>
            )}
          </Formik>)
  else
    return (<EntityLink 
      controller={"user"} 
      id={instance.user.id} 
      label={instance.nombres + " " + instance.apellidos}
      />)
  }

function Colaboradores({}){
  const { instance } = useInstance();

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
        {instance?.salida ? 
        <>
          <ContextTile
            title="Salidas"> 
            <DataTable
              items = {instance.salida}
              columns = {[
                {label: "Salida", controller: "salida", field: "id", tipo:ORCTableColumna.LINK_CONTROLADO},
                {label: "Fecha",  field: "fecha", tipo:ORCTableColumna.FECHA},
                {label: "Estado",  field: "estado_salida", tipo:ORCTableColumna.CADENA}
              ]}
              />         
          </ContextTile>
          <ContextTile title={"Visitas"}>
              <VisitaList filters={{salida__colaborador: instance.id}}/>
          </ContextTile>
        </>
      :[]}
      <ContextTile
      title={"Usuario"}
      >
        <User instance={instance}/>
      </ContextTile>
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
