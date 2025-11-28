import { useField } from "formik";
import { Form } from "react-bootstrap";

const PasswordFormik = ({ label, ...props }) => {
  const [field, meta] = useField(props);

  return (
    <Form.Group className="mb-3">
      {label && <Form.Label>{label}</Form.Label>}
      <Form.Control
        type="password"
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

export default PasswordFormik;
