import { useNavigate } from "react-router-dom";
import { useRouteMode } from "./useRouteMode";
import getAPIBase from "../api/BaseAPI";

export function useFormDelete({ controller }) {
  const navigate = useNavigate();
  const  {id} = useRouteMode();
  const { eliminar } = getAPIBase(controller);
  const redirectTo=`${controller}/`

  const handleDelete = async () => {
    await eliminar(id);
    alert("Registro eliminado");
    navigate(redirectTo);
  };

  return handleDelete;
}