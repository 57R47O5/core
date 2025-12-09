import { useState, useCallback } from "react";
import { useField } from "formik";
import { Form, ListGroup, Spinner } from "react-bootstrap";
import request from "../../api/requests";

export default function FormikAutocompleteRemote({
  name,
  endpoint,
  label,
  placeholder = "Escriba para buscar...",
  minLength = 2,
  delay = 300,
  ...props
}) {
  const [ field, meta, helpers] = useField(name);
  const { setValue } = helpers;

  const [texto, setTexto] = useState("");
  const [opciones, setOpciones] = useState([]);
  const [loading, setLoading] = useState(false);
  const [mostrarLista, setMostrarLista] = useState(false);

  // Debounce manual
  const debounce = (func, time) => {
    let timer;
    return (...args) => {
      clearTimeout(timer);
      timer = setTimeout(() => func(...args), time);
    };
  };

  const fetchOptions = async (query) => {
    if (query.length < minLength) {
      setOpciones([]);
      return;
    }

    setLoading(true);
    try {
      const resp = await request.get(`${endpoint}/options/?q=${query}`);
      setOpciones(resp ?? []);
    } catch (e) {
      console.error("Error en autocomplete", e);
      setOpciones([]);
    } finally {
      setLoading(false);
    }
  };

  // Debounced version
  const debouncedFetch = useCallback(debounce(fetchOptions, delay), []);

  const onChangeTexto = (e) => {
    const val = e.target.value;
    setTexto(val);
    debouncedFetch(val);
    setMostrarLista(true);
  };

  const onSeleccionar = (op) => {
    setValue(op.id);
    setTexto(op.descripcion);
    setMostrarLista(false);
  };

  return (
    <Form.Group className="mb-3" style={{ position: "relative" }}>
      {label && <Form.Label>{label}</Form.Label>}

      <Form.Control
        type="text"
        value={texto}
        placeholder={placeholder}
        onChange={onChangeTexto}
        onFocus={() => texto.length >= minLength && setMostrarLista(true)}
        isInvalid={meta.touched && meta.error}
        autoComplete="off"
        {...props}
      />

      {loading && (
        <Spinner
          animation="border"
          size="sm"
          style={{ position: "absolute", right: 10, top: 38 }}
        />
      )}

      {mostrarLista && opciones.length > 0 && (
        <ListGroup
          style={{
            position: "absolute",
            width: "100%",
            zIndex: 20,
            maxHeight: 200,
            overflowY: "auto",
          }}
        >
          {opciones.map((op) => (
            <ListGroup.Item
              key={op.id}
              action
              onClick={() => onSeleccionar(op)}
            >
              {op.descripcion}
            </ListGroup.Item>
          ))}
        </ListGroup>
      )}

      <Form.Control.Feedback type="invalid">
        {meta.error}
      </Form.Control.Feedback>
    </Form.Group>
  );
}
