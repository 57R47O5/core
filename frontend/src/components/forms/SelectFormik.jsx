import { useEffect, useState } from "react";
import { useField, useFormikContext } from "formik";
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
  const { values, setFieldValue } = useFormikContext();

  const [opciones, setOpciones] = useState([]);
  const [loading, setLoading] = useState(true);

  const value = values[name];

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

  // MODO EDICIÓN → mostrar EntityLink
  if (disabled && value) {
    const id = typeof value === "object" ? value.id : value;

    const displayLabel =
      typeof value === "object"
        ? value.label ?? value.descripcion
        : opciones.find((op) => op.id === value)?.descripcion;

    const controller =
      typeof value === "object"
        ? value.controller ?? endpoint
        : endpoint;

    return (
      <EntityLink
        id={id}
        label={displayLabel}
        controller={controller}
        fieldLabel={label}
      />
    );
  }

  // MODO NORMAL → Select
  return (
    <Form.Group className="mb-3">
      {label && <Form.Label>{label}</Form.Label>}

      <Form.Select
        {...field}
        {...props}
        value={
          typeof value === "object" && value !== null
            ? value.id
            : value ?? ""
        }
        onChange={(e) => {
          const selectedId = e.target.value;

          if (!selectedId) {
            setFieldValue(name, null);
            return;
          }

          const selectedObj = opciones.find(
            (op) => String(op.id) === String(selectedId)
          );

          // 🔥 Guardamos objeto completo (nuevo estándar)
          if (selectedObj) {
            setFieldValue(name, {
              id: selectedObj.id,
              label: selectedObj.label ?? selectedObj.descripcion,
              controller: selectedObj.controller ?? endpoint,
            });
          } else {
            // fallback viejo comportamiento
            setFieldValue(name, selectedId);
          }
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
