import { useEffect, useState } from "react";
import { useO2M } from "./O2MProvider";
import { Spinner } from "react-bootstrap";
import O2MTable from "./O2MTable";
import { Card } from "react-bootstrap";
import CenteredCard from "../displays/CenteredCard";
import './../../styles/cards.css'

export default function O2MInlineList({
  title,
  filtros,
}) {
  const {buscar, version} = useO2M();
  const [items, setItems] = useState([]);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    setCargando(true);
    buscar(filtros).then((data) => {
      setItems(data);
      setCargando(false);
    });
  }, [filtros, version]);

  if (cargando) return <Spinner />;

  return (
    <CenteredCard>
      {title && <h5 className="mt-4">{title}</h5>}
      <Card.Body>
      <O2MTable
        items={items}
        />
      </Card.Body>
    </CenteredCard>
  );
}
