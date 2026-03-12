import { useEffect, useState, useRef } from "react";
import DistritoElectoralForm from "./DistritoElectoralForm";
import CenteredCard from "../../../components/displays/CenteredCard";
import { Card, Spinner } from "react-bootstrap";
import { InstanceProvider, useInstance } from "../../../context/InstanceContext";
import { useRouteMode } from "../../../hooks/useRouteMode";
import getAPIBase from "../../../api/BaseAPI";
import AppMap, {FixMapSize} from "../../../components/geo/AppMap";
import MapGeoJSON from "../../../components/geo/MapGeoJson";
import "./../../../components/forms/map.css"


function DistritoElectoralView({}){
  const {id} = useRouteMode();
  const controller = "distrito-electoral"
  const {obtener} = getAPIBase(controller)
  const [center, setCenter] = useState(null);
  const [geometry, setGeometry] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const datos = await obtener(id);   
        setGeometry(datos.limites);
        setCenter(datos.centro)
      } catch (error) {
        console.error("Error al obtener datos:", error);
      }
    };

    if (id) {
      fetchData();
    }
  }, [id]);

  if (!geometry)
    return <><Spinner/></>
  else return (
      <AppMap center={center} zoom={11} >
        <MapGeoJSON geometry={geometry}/>
      </AppMap>
  )
}

function DistritosElectorales({}){
  const { instance } = useInstance();

  return (
    <>
    <CenteredCard>
      <Card.Body>
        <h3 className="mb-4 text-center">
          Distrito Electoral
        </h3>
      {instance ? <DistritoElectoralView/> : <DistritoElectoralForm/>}
      </Card.Body>
    </CenteredCard>
    </>
  );

}

export default function DistritoElectoralFormPage() {
  const {id} = useRouteMode();
  const controller = "distrito-electoral"
  return (
      <InstanceProvider
        controller={controller} 
        id = {id}     
      >
        <DistritosElectorales/>
        </InstanceProvider>
    );


}
