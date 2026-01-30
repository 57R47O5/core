import { useEffect, useState } from "react";
import { useO2M } from "./O2MProvider";
import { Spinner } from "react-bootstrap";
import O2MTable from "./O2MTable";

export default function O2MInlineList({
  title,
  filtros,
}) {
  const {buscar,} = useO2M();
  const [items, setItems] = useState([]);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    setCargando(true);
    buscar(filtros).then((data) => {
      setItems(data);
      setCargando(false);
    });
  }, [filtros]);

  if (cargando) return <Spinner />;

  return (
    <>
      {title && <h5 className="mt-4">{title}</h5>}

      <O2MTable
        items={items}
      />
    </>
  );
}
