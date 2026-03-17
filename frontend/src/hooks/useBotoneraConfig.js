import { useNavigate } from "react-router-dom";
import { useRouteMode } from "./useRouteMode";
import { useInstance } from "../context/InstanceContext";

export function useBotoneraConfig({
  onDelete,
  extraButtons = [],
}) {
  const { instance, controller } = useInstance();
  const navigate = useNavigate();
  const redirectTo = `${controller}/`
  const { isCreate } = useRouteMode();

  const config = {
    showSubmit: isCreate || instance?.capabilities?.editar,
    submitLabel: isCreate ? "Crear" : "Actualizar",
    showDelete: instance?.capabilities?.eliminar,
    onDelete,
    onCancel: () => navigate(redirectTo),
    extraButtons,
  };

  return config;
}