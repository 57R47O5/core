import { useNavigate } from "react-router-dom";
import getAPIBase from "../api/BaseAPI";

export function useFormDelete({ id, controller }) {
  const navigate = useNavigate();
  const { eliminar } = getAPIBase(controller);
  const redirectTo=`${controller}/`

  const handleDelete = async () => {
    await eliminar(id);
    alert("Registro eliminado");
    navigate(redirectTo);
  };

  return handleDelete;
}