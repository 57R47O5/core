import { useField } from "formik";
import { Form } from "react-bootstrap";

const CheckboxFormik = ({ label, ...props }) => {
  const [field, meta] = useField({ ...props, type: "checkbox" });

  return (
    <Form.Group className="mb-3">
      <Form.Check
        type="checkbox"
        label={label}
        {...field}
        {...props}
        isInvalid={meta.touched && meta.error}
      />
      {meta.touched && meta.error && (
        <Form.Control.Feedback type="invalid" style={{ display: "block" }}>
          {meta.error}
        </Form.Control.Feedback>
      )}
    </Form.Group>
  );
};

export default CheckboxFormik;
