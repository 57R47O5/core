import getAPIBase from "../../../api/BaseAPI";

const controller = "persona-user"
const {crear} = getAPIBase(controller)

export const colaboradorActions = {
  crear_usuario: {
    label: "Agregar Usuario",
    variant: "primary",
    action: async (instance, navigate) => {
      await crear("crear_usuario", instance.id);
      alert("Usuario creado");
    },
  },
};