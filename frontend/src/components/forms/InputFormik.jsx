import { useField } from "formik";
import { Form } from "react-bootstrap";

const InputFormik = ({ label, disabled = false, ...props }) => {
  const [field, meta] = useField(props);

  const showError = !disabled && meta.touched && meta.error;

  return (
    <Form.Group className="mb-3">
      {label && (
        <Form.Label className={disabled ? "text-muted" : ""}>
          {label}
        </Form.Label>
      )}

      <Form.Control
        {...field}
        {...props}
        disabled={disabled}
        isInvalid={showError}
      />

      {!disabled && (
        <Form.Control.Feedback type="invalid">
          {meta.error}
        </Form.Control.Feedback>
      )}
    </Form.Group>
  );
};

export default InputFormik;