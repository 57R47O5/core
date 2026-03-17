import { useNavigate } from "react-router-dom";
import { useRouteMode } from "./useRouteMode";
import getAPIBase from "../api/BaseAPI";

export function useFormSubmit({controller}) {
  const navigate = useNavigate();
  const  {id, isCreate} = useRouteMode();
  const { crear, editar } = getAPIBase(controller);
  const redirectTo=`${controller}/`


  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      if (isCreate) {
        await crear(values);
        alert("Registro creado");
      } else {
        await editar(id, values);
        alert("Registro actualizado");
      }
      navigate(redirectTo);
    } finally {
      setSubmitting(false);
    }
  };

  return handleSubmit;
}