import { Link } from "react-router-dom";
import { Form } from "react-bootstrap";

export default function EntityLink({ id, label, controller, fieldLabel }) {
  if (!id) return null;

  return (
    <Form.Group className="mb-3">
      {fieldLabel && <Form.Label>{fieldLabel}</Form.Label>}

      <Form.Control
        as={Link}
        to={`/${controller}/${id}/`}
        plaintext
        readOnly
        className="text-primary text-decoration-underline"
      >
        {label}
      </Form.Control>
    </Form.Group>
  );
}
