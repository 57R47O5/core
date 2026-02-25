
import { useMemo } from "react";
import { useModelForm } from "../../../hooks/useModelForm";
import { CampanaFields } from "./CampanaFields";
import { useRouteMode } from "../../../hooks/useRouteMode";

export default function CampanaForm() {
  const { isEdit } = useRouteMode();

      const dynamicFields = useMemo(() => ({
    ...CampanaFields,
    candidato: {
      ...CampanaFields.candidato,
      disabled: isEdit,
    },
    distrito: {
      ...CampanaFields.distrito,
      disabled: isEdit,
    },
    ciclo: {
      ...CampanaFields.ciclo,
      disabled: isEdit,
    },
  }), [isEdit]);

  const {FormFields} = useModelForm(dynamicFields);

  return (
  <>
    <FormFields/>
  </>
  );
} 
