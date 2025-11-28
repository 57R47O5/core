import { useEffect, useState } from "react";
import { useField } from "formik";
import { Form } from "react-bootstrap";
import request from "../../api/requests";

export default function SelectFormik({ name, endpoint, label, ...props }) {
  const [field, meta] = useField(name);
  const [opciones, setOpciones] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;

    const cargarOpciones = async () => {
      try {
        const respuesta = await request.get(`${endpoint}/options/`);
        if (isMounted) setOpciones(respuesta ?? []);
      } catch (err) {
        console.error(`Error cargando opciones de ${endpoint}`, err);
        if (isMounted) setOpciones([]);
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    cargarOpciones();

    return () => {
      isMounted = false;
    };
  }, [endpoint]);

  return (
    <Form.Group className="mb-3">
      {label && <Form.Label>{label}</Form.Label>}

      <Form.Select
        {...field}
        {...props}
        isInvalid={meta.touched && meta.error}
      >
        <option value="">
          {loading ? "Cargando..." : "-- Seleccione --"}
        </option>

        {!loading &&
          opciones.map((op) => (
            <option key={op.id} value={op.id}>
              {op.descripcion}
            </option>
          ))}
      </Form.Select>

      <Form.Control.Feedback type="invalid">
        {meta.error}
      </Form.Control.Feedback>
    </Form.Group>
  );
}
