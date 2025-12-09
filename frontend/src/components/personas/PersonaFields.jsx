import { Field } from "formik";
import {
  fieldContainerStyle,
  labelStyle,
  inputStyle,
  errorStyle,
} from "./PersonaFieldStyles";

const PersonaFields = ({ isReadOnly, errors, touched }) => (
  <>
    {/* Nombre */}
    <div style={fieldContainerStyle}>
      <label htmlFor="nombre" style={labelStyle}>Nombre:</label>
      <Field
        name="nombre"
        type="text"
        disabled={isReadOnly}
        style={inputStyle(isReadOnly)}
      />
      {errors.nombre && touched.nombre && (
        <div style={errorStyle}>{errors.nombre}</div>
      )}
    </div>

    {/* Documento */}
    <div style={fieldContainerStyle}>
      <label htmlFor="documento" style={labelStyle}>Documento:</label>
      <Field
        name="documento"
        type="text"
        disabled={isReadOnly}
        style={inputStyle(isReadOnly)}
      />
      {errors.documento && touched.documento && (
        <div style={errorStyle}>{errors.documento}</div>
      )}
    </div>

    {/* Teléfono */}
    <div style={fieldContainerStyle}>
      <label htmlFor="telefono" style={labelStyle}>Teléfono:</label>
      <Field
        name="telefono"
        type="text"
        disabled={isReadOnly}
        style={inputStyle(isReadOnly)}
      />
      {errors.telefono && touched.telefono && (
        <div style={errorStyle}>{errors.telefono}</div>
      )}
    </div>

    {/* Usuario */}
    <div style={fieldContainerStyle}>
      <label htmlFor="usuario" style={labelStyle}>Usuario:</label>
      <Field
        name="usuario"
        type="text"
        disabled={true} // siempre deshabilitado
        style={inputStyle(true)}
      />
    </div>

    {/* Email */}
    <div style={fieldContainerStyle}>
      <label htmlFor="email" style={labelStyle}>Email:</label>
      <Field
        name="email"
        type="email"
        disabled={true} // siempre deshabilitado
        style={inputStyle(true)}
      />
    </div>
  </>
);

export default PersonaFields;
