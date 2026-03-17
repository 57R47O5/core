import { useRouteMode } from "./useRouteMode";
import { useInstance } from "../context/InstanceContext";

export function resolveInitialValues({
  formModel,
  FormComponent,
  context,
}) {
  const { instance } = useInstance();
  const { isEdit } = useRouteMode();

  // 1. instancia existente
  if (isEdit && instance) {
    return instance;
  }

  // 2. defaults del modelo
  const defaults = formModel.baseInitialValues || {};

  // 3. contexto (sobrescribe)
  const contextValues =
    FormComponent.getContextValues?.(context) || {};

  return {
    ...defaults,
    ...contextValues,
  };
};
