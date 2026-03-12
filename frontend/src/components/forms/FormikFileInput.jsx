import React, { useRef, useEffect } from "react";
import { useField } from "formik";

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
    <div className="form-field">
      {label && <label htmlFor={name}>{label}</label>}

      <input
        ref={inputRef}
        id={name}
        name={name}
        type="file"
        accept={accept}
        multiple={multiple}
        onChange={handleChange}
      />

      {meta.touched && meta.error && (
        <div className="form-error">{meta.error}</div>
      )}

      {field.value && !multiple && (
        <div className="file-preview">
          {field.value.name}
        </div>
      )}

      {multiple && Array.isArray(field.value) && (
        <ul>
          {field.value.map((file, i) => (
            <li key={i}>{file.name}</li>
          ))}
        </ul>
      )}
    </div>
  );
}