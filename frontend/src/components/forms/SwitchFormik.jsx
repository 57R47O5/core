import { useField } from "formik";
import { Form } from "react-bootstrap";

const SwitchFormik = ({ label, ...props }) => {
  const [field, meta, helpers] = useField({ ...props, type: "checkbox" });

  return (
    <Form.Group className="mb-3">
      <Form.Check 
        type="switch"
        id={props.id || props.name}
        label={label}
        checked={field.value}
        onChange={(e) => helpers.setValue(e.target.checked)}
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

export default SwitchFormik;
