import { Form } from "react-bootstrap";
import BaseLink from "../displays/BaseLink";
import "./field-link.css";

export default function FieldLink({
  to,
  label,
  fieldLabel,
}) {
  return (
    <Form.Group className="mb-3">
      {fieldLabel && <Form.Label>{fieldLabel}</Form.Label>}

      <div className="form-plaintext-wrapper">
        <BaseLink to={to} variant="muted">
          {label}
        </BaseLink>
      </div>
    </Form.Group>
  );
}