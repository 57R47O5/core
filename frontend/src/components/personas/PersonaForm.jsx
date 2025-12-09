import { useReducer } from "react";
import { Formik, Form } from "formik";
import * as Yup from "yup";
import PersonaFields from "./PersonaFields";
import {
  createPersona,
  updatePersona,
  deletePersona,
} from "../../api/PersonasAPI";

// --- Reducer para manejar los modos ---
function modeReducer(state, action) {
  switch (action.type) {
    case "SET_MODE":
      return { ...state, mode: action.payload };
    default:
      return state;
  }
}

// --- Componente principal ---
const PersonaForm = ({ user, datosPersona = null, onSuccess }) => {
  const [state, dispatch] = useReducer(modeReducer, {
    mode: datosPersona ? "visualizacion" : "creacion",
  });

  const { mode } = state;

  const initialValues = {
    nombre: datosPersona?.nombre || "",
    documento: datosPersona?.documento || "",
    telefono: datosPersona?.telefono || "",
    email: datosPersona?.email || user?.email || "",
    usuario: datosPersona?.usuario || user?.username || "",
  };

  const validationSchema = Yup.object({
    nombre: Yup.string()
      .required("El nombre es obligatorio")
      .max(255, "Máximo 255 caracteres"),
    documento: Yup.string().max(12, "Máximo 12 caracteres"),
    telefono: Yup.string(),
  });

  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      let data = null;

      if (mode === "creacion") {
        data = await createPersona({
          ...values,
          usuario: user.id,
        });
      } else if (mode === "edicion" && datosPersona?.id) {
        data = await updatePersona(datosPersona.id, values);
      }

      if (data) {
        onSuccess?.();
        dispatch({ type: "SET_MODE", payload: "visualizacion" });
      }
    } catch (error) {
      console.error("Error en el formulario de persona:", error);
      alert("Ocurrió un error al guardar los datos de la persona.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async () => {
    if (!datosPersona?.id) return;
    const confirmDelete = window.confirm(
      "¿Seguro que deseas eliminar esta persona?"
    );
    if (!confirmDelete) return;

    try {
      const deleted = await deletePersona(datosPersona.id);
      if (deleted) {
        alert("Persona eliminada correctamente.");
        onSuccess?.();
        dispatch({ type: "SET_MODE", payload: "creacion" });
      }
    } catch (error) {
      console.error("Error eliminando persona:", error);
      alert("No se pudo eliminar la persona.");
    }
  };

  const isReadOnly = mode === "visualizacion";

  return (
    <div style={{ border: "1px solid #ddd", padding: 20, borderRadius: 10 }}>
      <h3>
        {mode === "creacion"
          ? "Crear Persona"
          : mode === "edicion"
          ? "Editar Persona"
          : "Datos de Persona"}
      </h3>

      <Formik
        initialValues={initialValues}
        validationSchema={validationSchema}
        onSubmit={handleSubmit}
        enableReinitialize
      >
        {({ errors, touched, isSubmitting }) => (
          <Form>
            <PersonaFields
              isReadOnly={isReadOnly}
              errors={errors}
              touched={touched}
            />

            <div style={{ marginTop: 15 }}>
              {!isReadOnly && (
                <button type="submit" disabled={isSubmitting}>
                  {isSubmitting
                    ? "Guardando..."
                    : mode === "creacion"
                    ? "Crear Persona"
                    : "Guardar Cambios"}
                </button>
              )}

              {isReadOnly && (
                <button
                  type="button"
                  onClick={() =>
                    dispatch({ type: "SET_MODE", payload: "edicion" })
                  }
                  style={{ marginRight: 10 }}
                >
                  Editar
                </button>
              )}

              {mode === "edicion" && (
                <button
                  type="button"
                  onClick={handleDelete}
                  style={{ marginLeft: 10, backgroundColor: "red", color: "white" }}
                >
                  Eliminar
                </button>
              )}
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default PersonaForm;
