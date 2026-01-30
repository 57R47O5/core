import * as Yup from "yup";

export function buildInitialValues(fields) {
  return Object.fromEntries(
    Object.entries(fields).map(([name, def]) => [
      name,
      def.initial ?? "",
    ])
  );
}

export function buildValidationSchema(fields) {
  return Yup.object(
    Object.fromEntries(
      Object.entries(fields).map(([name, def]) => [
        name,
        def.validation,
      ])
    )
  );
}

export function buildColumnsFromFields(fields) {
  return Object.entries(fields).map(([name, def]) => ({
    label: def.label,
    field: name,
    render: ({ formik }) =>
      def.render({
        name,
        value: formik.values[name] ?? "",
        onChange: formik.handleChange,
      }),
  }));
}

export function buildFormFields(fields, order = null) {
  const entries = order
    ? order.map((k) => [k, fields[k]])
    : Object.entries(fields);

  return function FormFields() {
    return (
      <>
        {entries.map(([name, def]) =>
          def.render({ name, label: def.label })
        )}
      </>
    );
  };
}
