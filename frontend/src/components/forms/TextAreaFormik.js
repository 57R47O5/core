import { useField } from "formik";
import { Form } from "react-bootstrap";

const TextareaFormik = ({ label, rows = 3, ...props }) => {
  const [field, meta] = useField(props);

  return (
    <Form.Group className="mb-3">
      {label && <Form.Label>{label}</Form.Label>}

      <Form.Control
        as="textarea"
        rows={rows}
        {...field}
        {...props}
        isInvalid={meta.touched && meta.error}
      />

      <Form.Control.Feedback type="invalid">
        {meta.error}
      </Form.Control.Feedback>
    </Form.Group>
  );
};

export default TextareaFormik;
