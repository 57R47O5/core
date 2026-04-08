import { useNavigate } from "react-router-dom";
import getAPIBase from "../api/BaseAPI";

export function useFormSubmit({id, exists, controller}) {
  const navigate = useNavigate();
  const { crear, editar } = getAPIBase(controller);
  const redirectTo=`${controller}/`
  const  isCreate = !exists;


  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      if (isCreate) {
        const response = await crear(values);
        const newId = response?.id;
        alert("Registro creado");
        navigate(`/${controller}/${newId}/`);
      } else {
        await editar(id, values);
        alert("Registro actualizado");
        navigate(`/${controller}/${id}/`);
      }
    } finally {
      setSubmitting(false);
    }
  };

  return handleSubmit;
}