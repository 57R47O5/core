import { useEffect, useState } from "react";
import ReactSpeedometer from "react-d3-speedometer";
import {  WordCloud } from "@isoterik/react-word-cloud";
import "./dashboard.css"

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from "recharts";

import { Card, Row, Col, Spinner } from "react-bootstrap";
import  getAPIBase from "../../../api/BaseAPI";

function EvolucionTemporal({visitasTiempo}){
  return (
        <Col md={8}>
          <Card className="shadow-sm dashboard-card">
            <Card.Body>

              <h6 className="text-muted mb-3">
                Visitas acumuladas
              </h6>

              <ResponsiveContainer width="100%" height={300}>

                <LineChart data={visitasTiempo}>

                  <CartesianGrid strokeDasharray="3 3" />

                  <XAxis dataKey="fecha" />

                  <YAxis />

                  <Tooltip />

                  <Line
                    type="monotone"
                    dataKey="count"
                    stroke="#0d6efd"
                    strokeWidth={3}
                  />

                </LineChart>

              </ResponsiveContainer>

            </Card.Body>
          </Card>
        </Col>
  );

}

function TotalVisitas({data}){
  return ( <Col md={3}>
          <Card className="shadow-sm dashboard-card">
            <Card.Body>
              <h6 className="text-muted">Total de visitas</h6>
              <h1 style={{ textAlign: "center" }}>{data.total_visitas}</h1>
            </Card.Body>
          </Card>
        </Col>

  )
};

const RESULTADO_LABELS = [
  "Rechazo",
  "Regular",
  "Interés",
  "Promesa de Voto"
];

function ResultadoPromedio({data}){

  const labelActual =
  RESULTADO_LABELS[Math.round(data.resultado_promedio) - 1] ?? "";
  return (<Col md={9}>
          <Card className="dashboard-card">
            <Card.Body>

              <h6 className="text-muted mb-3">
                Resultado de visitas
              </h6>

              <div className="d-flex justify-content-center">

              <ReactSpeedometer
                value={data.resultado_promedio}
                minValue={1}
                maxValue={4}
                segments={4}

                needleColor="black"

                startColor="#d73027"
                endColor="#1a9850"

                height={220}

                currentValueText={`Resultado: ${labelActual}`}

                customSegmentLabels={[
                  {
                    text: "Rechazo",
                    position: "INSIDE",
                    color: "#fff",
                    fontSize: "12px",
                  },
                  {
                    text: "Regular",
                    position: "INSIDE",
                    color: "#fff",
                    fontSize: "12px",
                  },
                  {
                    text: "Interés",
                    position: "INSIDE",
                    color: "#fff",
                    fontSize: "12px",
                  },
                  {
                    text: "Promesa de voto",
                    position: "INSIDE",
                    color: "#fff",
                    fontSize: "12px",
                  },
                ]}
              />

              </div>
            </Card.Body>
          </Card>
        </Col>
        )
};

function ElWordCloud({data}){

  const options = {
    rotations: 2,
    rotationAngles: [-90, 0],
  };

  return (<Col md={4}>
          <Card className="shadow-sm dashboard-card">
            <Card.Body>

              <h6 className="text-muted mb-3">
                Preocupaciones ciudadanas
              </h6>
              {Array.isArray(data.wordcloud) && data.wordcloud.length > 0 ? (

              <WordCloud words={data.wordcloud} width={300} height={200} />
              ) : null}

            </Card.Body>
          </Card>
        </Col>
  )
};

function TemasDetectados({data}){
  return (<Col md={12}>
          <Card className="shadow-sm dashboard-card">
            <Card.Body>

              <h6 className="text-muted mb-3">
                Temas detectados automáticamente
              </h6>

              <Row>

                {data.temas.map((tema) => (

                  <Col md={3} key={tema.tema}>

                    <Card className="mb-3 border-0 bg-light">

                      <Card.Body>

                        <strong>Tema {tema.tema + 1}</strong>

                        <div className="mt-2">

                          {tema.palabras.map((p) => (
                            <span
                              key={p}
                              className="badge bg-secondary me-1 mb-1"
                            >
                              {p}
                            </span>
                          ))}

                        </div>

                      </Card.Body>

                    </Card>

                  </Col>

                ))}

              </Row>

            </Card.Body>
          </Card>
        </Col>

  )};

export default function AnaliticaDashboardPage() {

  const { listar } = getAPIBase("api/analitica");
  const [data, setData] = useState(null);

  useEffect(() => {
    async function cargar() {
      const res = await listar();
      setData(res);
    }
    cargar();
  }, []);

  if (!data) {
    return (
      <div className="text-center mt-5">
        <Spinner />
      </div>
    );
  }


  const visitasTiempo = data.visitas_acumuladas_por_fecha;

  return (
    <div className="container-fluid p-4 dashboard">

      <Row className="mb-4">

        {/* TOTAL VISITAS */}

        <TotalVisitas data={data} />
        {/* RESULTADO PROMEDIO */}
        <ResultadoPromedio data={data} />

      </Row>

      <Row className="mb-4">

        {/* EVOLUCIÓN TEMPORAL */}
        <EvolucionTemporal visitasTiempo={visitasTiempo} />

        {/* WORD CLOUD */}
        <ElWordCloud data={data} />

      </Row>

      <Row>

        {/* TEMAS DETECTADOS */}
        {/* <TemasDetectados data={data} /> */}

      </Row>

    </div>
  );
}
