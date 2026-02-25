
import { useModelForm } from "../../../hooks/useModelForm";
import { CampanaFields } from "./CampanaFields";
import { useRouteMode } from "../../../hooks/useRouteMode";

export default function CampanaForm() {
  const { isEdit } = useRouteMode();

    const dynamicFields = {
    ...CampanaFields,
    candidato: {
      ...CampanaFields.candidato,
      disabled: isEdit,
    },
    distrito: {
      ...CampanaFields.distrito,
      disabled: isEdit,
    },
  };

  const {FormFields} = useModelForm(dynamicFields);

  return (
  <>
    <FormFields/>
  </>
  );
} 
