import React, { useRef, useEffect } from "react";
import { useField } from "formik";
import "./field-file.css"
import * as Icons from "react-icons/fa";

export default function FormikFileInput({
  name,
  label,
  accept,
  multiple = false,
  onChange
}) {
  const [field, meta, helpers] = useField(name);
  const inputRef = useRef(null);

  useEffect(() => {
    if (!field.value && inputRef.current) {
      inputRef.current.value = "";
    }
  }, [field.value]);

  const handleChange = (event) => {
    const files = event.target.files;

    const value = multiple
      ? Array.from(files)
      : files[0];

    helpers.setValue(value);

    if (onChange) {
      onChange(value);
    }
  };

return (
  <div className="form-field file-field">
    {label && <label className="file-label" htmlFor={name}>{label}</label>}

    <div
      className={`file-input-wrapper ${field.value ? "has-file" : ""}`}
      onClick={() => inputRef.current.click()}
    >
      <input
        ref={inputRef}
        id={name}
        name={name}
        type="file"
        accept={accept}
        multiple={multiple}
        onChange={handleChange}
        className="file-input-hidden"
      />

      <div className="file-input-content">
        <Icons.FaFileAlt size={30} color="#243f56"/>
        <div className="file-text">
          <span className="file-primary">
            {multiple ? "Seleccionar archivos" : "Seleccionar archivo"}
          </span>
          <span className="file-secondary">
            o arrastrar y soltar
          </span>
        </div>
      </div>
    </div>

    {meta.touched && meta.error && (
      <div className="form-error">{meta.error}</div>
    )}

    {field.value && !multiple && (
      <div className="file-preview">
        {field.value.name}
      </div>
    )}

    {multiple && Array.isArray(field.value) && (
      <ul className="file-list">
        {field.value.map((file, i) => (
          <li key={i}>{file.name}</li>
        ))}
      </ul>
    )}
  </div>
);
}