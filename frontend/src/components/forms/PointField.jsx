import { useField } from "formik";

export default function PointField({ name }) {
  const [field, , helpers] = useField(name);

  return (
    <>
      <MapPointPicker
        value={field.value}
        onChange={helpers.setValue}
      />

      <UseCurrentLocation onChange={helpers.setValue} />
    </>
  );
}
