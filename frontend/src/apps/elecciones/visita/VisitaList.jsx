import { useState, useEffect } from "react"
import AppMap from "../../../components/geo/AppMap"
import MapPoints from "../../../components/geo/MapPoints"
import getAPIBase from "../../../api/BaseAPI"
import { DataTable, ORCTableColumna } from "../../../components/listados/DataTable"
import { control } from "leaflet"

export function createColorScale(field, scale) {
  return (row) => scale[row[field]] || "#999";
}

const resultadoScale = createColorScale("resultado_id", {
  1: "#d73027",
  2: "#fc8d59",
  3: "#fee08b",
  4: "#1a9850"
});


/**
 * VisitaList
 *
 * Componente que muestra las visitas de una salida en un mapa.
 * Los resultados de las visitas se muestran en escala de colores
 * 
 * Props:
 * - filter: obj {salida: id}
 * 
 */
export default function VisitaList({filters, mode = "mapa"}) {
    const { buscar } = getAPIBase("visita")

    const [items, setItems] = useState([])  
    useEffect(() => {
        buscar(filters).then(setItems)
    }, [filters])

    if (mode === "lista") {
         return (MostrarLista(items))
    }
    return (MostrarMapa(items)
  )
}

function MostrarMapa(items) {
  const position = [-25.2637, -57.5759];
  return <AppMap center={position} zoom={13}>
    <MapPoints
      data={items}
      getColor={resultadoScale} />
  </AppMap>;
}

function MostrarLista(items) {
    return <DataTable
        items={items}
        columns={[ 
            { label: "Votante", field: "votante_id", fieldDisplay: "votante",
              controller: "votante", tipo: ORCTableColumna.LINK_CONTROLADO},
            { label: "Fecha", field: "fecha", tipo: ORCTableColumna.FECHA_HORA },
            { label: "Resultado", field: "resultado" }
        ]}
    />    
  }

