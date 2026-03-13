import { useState, useEffect } from "react"
import AppMap from "../../../components/geo/AppMap"
import MapPoints from "../../../components/geo/MapPoints"
import getAPIBase from "../../../api/BaseAPI"

export function createColorScale(field, scale) {
  return (row) => scale[row[field]] || "#999";
}

const resultadoScale = createColorScale("resultado_id", {
  1: "#d73027",
  2: "#fc8d59",
  3: "#fee08b",
  4: "#1a9850"
});

export default function VisitaList({filters}) {
    const { buscar } = getAPIBase("visita")

    const [items, setItems] = useState([])  
    useEffect(() => {
        buscar(filters).then(setItems)
    }, [filters])

    const position = [-25.2637, -57.5759];

    return (
              <AppMap center={position} zoom={13}>
                <MapPoints
                  data={items}
                  getColor={resultadoScale}
                />
              </AppMap> )
}
