import { useEffect, useState } from "react";
import { useField } from "formik";
import { Form } from "react-bootstrap";
import request from "../../api/requests";
import EntityLink from "../displays/EntityLink";

export default function SelectFormik({
  name,
  endpoint,
  label,
  disabled = false,
  ...props
}) {
  const [field, meta, helpers] = useField(name);

  const [opciones, setOpciones] = useState([]);
  const [loading, setLoading] = useState(true);

  const value = field.value;

  // Cargar opciones
  useEffect(() => {
    let isMounted = true;

    const cargarOpciones = async () => {
      try {
        const respuesta = await request.get(`${endpoint}/`);
        if (isMounted) setOpciones(respuesta ?? []);
      } catch (err) {
        console.error(`Error cargando opciones de ${endpoint}`, err);
        if (isMounted) setOpciones([]);
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    if (!disabled) {
      cargarOpciones();
    }

    return () => {
      isMounted = false;
    };
  }, [endpoint, disabled]);

  const selectedOption = opciones.find(
    (op) => String(op.id) === String(value)
  );

  if (disabled && value) {
    return (
      <EntityLink
        id={value.id}
        label={value.label ?? value.descripcion }
        controller={endpoint}
        fieldLabel={label}
      />
    );
  }

  return (
    <Form.Group className="mb-3">
      {label && <Form.Label>{label}</Form.Label>}

      <Form.Select
        {...field}
        {...props}
        value={value ?? ""}
        onChange={(e) => {
          const selectedId = e.target.value || null;
          helpers.setValue(selectedId);
        }}
        isInvalid={meta.touched && meta.error}
      >
        <option value="">
          {loading ? "Cargando..." : "-- Seleccione --"}
        </option>

        {!loading &&
          opciones.map((op) => (
            <option key={op.id} value={op.id}>
              {op.label ?? op.descripcion}
            </option>
          ))}
      </Form.Select>

      <Form.Control.Feedback type="invalid">
        {meta.error}
      </Form.Control.Feedback>
    </Form.Group>
  );
}