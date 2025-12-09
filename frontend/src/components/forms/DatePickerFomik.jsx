import { useField } from "formik";
import { Form } from "react-bootstrap";

/**
 * mode:
 *   - "date": solo fecha (YYYY-MM-DD)
 *   - "datetime": fecha y hora (YYYY-MM-DDTHH:MM)
 */
const DatepickerFormik = ({ label, mode = "date", ...props }) => {
  const [field, meta, helpers] = useField(props);

  const isDateOnly = mode === "date";

  /** Convertimos el valor ISO → formato que entiende el input */
  const formatForInput = (value) => {
    if (!value) return "";

    const date = new Date(value);

    if (isDateOnly) {
      return date.toISOString().split("T")[0]; // YYYY-MM-DD
    }

    // YYYY-MM-DDTHH:MM
    const iso = date.toISOString();
    return iso.slice(0, 16);
  };

  /** Cuando el usuario selecciona algo en el input */
  const handleChange = (e) => {
    const raw = e.target.value; // "YYYY-MM-DD" o "YYYY-MM-DDTHH:MM"
    if (!raw) {
      helpers.setValue("");
      return;
    }

    let dateWithTZ;

    if (isDateOnly) {
      // Crear fecha con TZ local correctamente
      const [y, m, d] = raw.split("-");
      dateWithTZ = new Date(Number(y), Number(m) - 1, Number(d));
    } else {
      // YYYY-MM-DDTHH:MM → separar fecha y hora
      const [datePart, timePart] = raw.split("T");
      const [y, m, d] = datePart.split("-");
      const [hh, mm] = timePart.split(":");

      dateWithTZ = new Date(
        Number(y),
        Number(m) - 1,
        Number(d),
        Number(hh),
        Number(mm)
      );
    }

    helpers.setValue(dateWithTZ.toISOString());
  };

  return (
    <Form.Group className="mb-3">
      {label && <Form.Label>{label}</Form.Label>}

      <Form.Control
        type={isDateOnly ? "date" : "datetime-local"}
        value={formatForInput(field.value)}
        onChange={handleChange}
        onBlur={field.onBlur}
        isInvalid={meta.touched && meta.error}
        {...props}
      />

      <Form.Control.Feedback type="invalid">
        {meta.error}
      </Form.Control.Feedback>
    </Form.Group>
  );
};

export default DatepickerFormik;
