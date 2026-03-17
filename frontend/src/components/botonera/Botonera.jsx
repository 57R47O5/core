import { Button, Spinner } from "react-bootstrap";
import { useFormikContext } from "formik";
import { Alertar, Tipo } from "../../utils/alertas";

export default function Botonera({
  onDelete,
  onCancel,
  showDelete = true,
  submitLabel = "Guardar",
  extraButtons,
}) {
  const { validateForm, submitForm, isSubmitting, validationSchema } = useFormikContext();

    const handleSafeSubmit = async () => {
    const errors = await validateForm();

    if (Object.keys(errors).length > 0) {
      const firstError = Object.values(errors)[0];
      Alertar(firstError, Tipo.ERROR, "Error");
      return;
    }

    submitForm();
  };

  return (
    <div className="d-flex gap-2">

      {/* GUARDAR */}
      {showDelete && <Button
        variant="primary"
        onClick={handleSafeSubmit}
        disabled={isSubmitting}
      >
        {isSubmitting ? (
          <>
            <Spinner
              as="span"
              animation="border"
              size="sm"
              className="me-2"
            />
            Guardando...
          </>
        ) : (
          <>
            <i className="fa fa-save me-2" />
            {submitLabel}
          </>
        )}
      </Button>}

      {/* ELIMINAR */}
      {showDelete && onDelete && (
        <Button
          variant="danger"
          onClick={onDelete}
          disabled={isSubmitting}
        >
          <i className="fa fa-trash-alt me-2" />
          Eliminar
        </Button>
      )}

      {/* VOLVER */}
      {onCancel && (
        <Button
          variant="secondary"
          onClick={onCancel}
          disabled={isSubmitting}
        >
          <i className="fas fa-arrow-left me-2" />
          Volver
        </Button>
      )}
      {/* Botones Extra */}
      {extraButtons?.map((btn, index) => (
        <Button
          key={index}
          variant={btn.variant}
          onClick={btn.onClick}
        >
          {btn.label}
        </Button>
      ))}
    </div>
  );
}