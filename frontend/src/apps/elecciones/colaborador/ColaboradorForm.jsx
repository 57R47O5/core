
import { useMemo } from "react";
import { useModelForm } from "../../../hooks/useModelForm";
import { ColaboradorFields } from "./ColaboradorFields";
import getAPIBase from "../../../api/BaseAPI";
import { useRouteMode } from "../../../hooks/useRouteMode";

function ColaboradorForm() {
  const { isEdit } = useRouteMode();
  
  const dynamicFields = useMemo(() => ({
      ...ColaboradorFields,
      user: {
        ...ColaboradorFields.user,
        disabled: isEdit,
      },
    }), [isEdit]);

  const {FormFields} = useModelForm(dynamicFields
  );  
    
  return (
    <FormFields/>     
  );
} 

ColaboradorForm.actions = ({ instance, formik, api, navigate }) => ({


  crear_usuario: {
    label: "Agregar Usuarios",
    variant: "primary",
    action: async () => {
      const api = getAPIBase("persona-user");
      const { crear } = api;

      await crear(formik.values);
    },
  },
});

export default ColaboradorForm;