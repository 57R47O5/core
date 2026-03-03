import FieldLink from "../forms/FieldLink";

export default function EntityLink({
  controller,
  id,
  label,
  fieldLabel,
}) {
  return (
    <FieldLink
      to={`/${controller}/${id}/`}
      label={label}
      fieldLabel={fieldLabel}
    />
  );
}