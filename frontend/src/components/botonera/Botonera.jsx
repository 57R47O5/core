import React from "react";
import { Button, Spinner } from "react-bootstrap";
import { useFormikContext } from "formik";

export default function Botonera({
  showSubmit,
  onDelete,
  onCancel,
  showDelete = true,
  submitLabel = "Guardar",
  extraButtons,
}) {
  const { submitForm, isSubmitting } = useFormikContext();

  return (
    <div className="d-flex gap-2">

      {/* GUARDAR */}
      {showDelete && <Button
        variant="primary"
        onClick={submitForm}
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