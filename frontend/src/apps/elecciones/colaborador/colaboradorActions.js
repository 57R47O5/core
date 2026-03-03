import { useInstance } from "../../../context/InstanceContext";

export function useColaboradorActions() {
  //const instance = useInstance();

  async function crearUsuario(navigate) {
    await crear("crear_usuario", instance.id);
    alert("Usuario creado");
  }

  return {
    crear_usuario: {
      label: "Agregar Usuario",
      variant: "primary",
      action: crearUsuario,
    },
  };
}
