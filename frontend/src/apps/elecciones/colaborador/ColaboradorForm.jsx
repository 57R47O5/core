
import { useMemo } from "react";
import { useModelForm } from "../../../hooks/useModelForm";
import { ColaboradorFields } from "./ColaboradorFields";
import getAPIBase from "../../../api/BaseAPI";
import { useRouteMode } from "../../../hooks/useRouteMode";
import { useInstance } from "../../../context/InstanceContext";

function ColaboradorForm() {
  
  const {FormFields} = useModelForm(ColaboradorFields
  );  
    
  return (
    <FormFields/>     
  );
} 


export default ColaboradorForm;