import * as Yup from "yup";


export const UsuarioSchema = (isEdit) =>
  Yup.object().shape({
    username: Yup.string().required("El nombre de usuario es obligatorio"),

    email: Yup.string()
      .email("Formato de email inválido")
      .required("El email es obligatorio"),

    rol: Yup.string()
      .oneOf(["medico", "secretaria"])
      .required("El rol es obligatorio"),

    // Contraseña: solo obligatoria en creación
    password: isEdit
      ? Yup.string().nullable()
      : Yup.string()
          .required("La contraseña es obligatoria")
          .min(6, "La contraseña debe tener al menos 6 caracteres"),

    password2: isEdit
      ? Yup.string().nullable()
      : Yup.string()
          .required("Debe repetir la contraseña")
          .oneOf([Yup.ref("password"), null], "Las contraseñas no coinciden"),
  });
