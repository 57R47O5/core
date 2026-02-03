import { useMemo } from "react";
import { Field, Form as RBForm } from "formik";
import * as Yup from "yup";

export function useModelForm(fields, order = null) {
  
  const entries = useMemo(() => {
    return order
    ? order.map((k) => [k, fields[k]])
    : Object.entries(fields);
  }, [fields, order]);
  
  const initialValues = useMemo(() => {
    return Object.fromEntries(
      entries.filter(([_, def]) => def.form === true)
      .map(([name, def]) => [
        name,
        def.initial ?? "",
      ])
    );
  }, [entries]);

  const initialValuesFilter = useMemo(() => {
    return Object.fromEntries(
      entries.filter(([_, def]) => def.filter === true)
      .map(([name, def]) => [
        name,
        def.initial ?? "",
      ])
    );
  }, [entries]);

  const validationSchema = useMemo(() => {
    return Yup.object(
      Object.fromEntries(
        entries.filter(([_, def]) => def.form === true)
        .map(([name, def]) => [
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

  const FormFields  = useMemo(() => {
    return function FormFields() {
      return (
        <>
          {entries
          .filter(([, def]) => def.form)
          .map(([name, def]) =>
            def.render({
              name,
              label: def.label,
            })
          )}
        </>
      );
    };
  }, [entries]);

  const FilterFields = useMemo(() => {
    return function FilterFields() {
      return (
        <>
          {entries
            .filter(([, def]) => def.filter)
            .map(([name, def]) => (
              <div className="col-md-3 mb-3" key={name}>
                {def.render({
                  name,
                  label: def.label,
                })}
              </div>
            ))}
        </>
      );
    };
  }, [entries]);

  return {
    fields,
    entries,
    initialValues,
    initialValuesFilter,
    validationSchema,
    columns,
    FormFields,
    FilterFields
  };
}