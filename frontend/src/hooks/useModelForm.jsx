import { useMemo } from "react";
import * as Yup from "yup";

export function useModelForm(fields, order = null) {
  const entries = useMemo(() => {
    return order
      ? order.map((k) => [k, fields[k]])
      : Object.entries(fields);
  }, [fields, order]);

  const initialValues = useMemo(() => {
    return Object.fromEntries(
      entries.map(([name, def]) => [
        name,
        def.initial ?? "",
      ])
    );
  }, [entries]);

  const validationSchema = useMemo(() => {
    return Yup.object(
      Object.fromEntries(
        entries.map(([name, def]) => [
          name,
          def.validation,
        ])
      )
    );
  }, [entries]);

  const columns = useMemo(() => {
    return entries.map(([name, def]) => ({
      label: def.label,
      field: name,
      render: ({ formik }) =>
        def.render({
          name,
          value: formik.values[name] ?? "",
          onChange: formik.handleChange,
        }),
    }));
  }, [entries]);

  const FormFields = useMemo(() => {
    return function FormFields() {
      return (
        <>
          {entries.map(([name, def]) =>
            def.render({
              name,
              label: def.label,
            })
          )}
        </>
      );
    };
  }, [entries]);

  return {
    fields,
    entries,
    initialValues,
    validationSchema,
    columns,
    FormFields,
  };
}
