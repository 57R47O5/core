import "./../index.css";
import { useNavigate } from "react-router-dom";
import { register } from "../api/auth";
import { useFormik } from "formik";
import * as Yup from "yup";

const Register = () => {
  const navigate = useNavigate();

  const formik = useFormik({
    initialValues: {
      username: "",
      email: "",
      password: "",
      password2: "",
    },

    validationSchema: Yup.object({
      username: Yup.string()
        .min(3, "Mínimo 3 caracteres")
        .required("Requerido"),

      email: Yup.string()
        .email("Email inválido")
        .required("Requerido"),

      password: Yup.string()
        .min(6, "Mínimo 6 caracteres")
        .required("Requerido"),

      password2: Yup.string()
        .oneOf([Yup.ref("password")], "Las contraseñas no coinciden")
        .required("Requerido"),
    }),

    onSubmit: async (values, { setSubmitting, setStatus }) => {
      setStatus(null);

      try {
        const payload = {
          username: values.username,
          email: values.email,
          password: values.password,
        };

        await register(payload);
        navigate("/login");
      } catch (err) {
        console.error(err);
        setStatus("Error al registrar el usuario. Verifica los datos.");
      } finally {
        setSubmitting(false);
      }
    },
  });

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Crear cuenta</h2>

      <form onSubmit={formik.handleSubmit} style={styles.form}>
        {/* USERNAME */}
        <input
          type="text"
          name="username"
          placeholder="Nombre de usuario"
          value={formik.values.username}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          style={styles.input}
        />
        {formik.touched.username && formik.errors.username && (
          <p style={styles.error}>{formik.errors.username}</p>
        )}

        {/* EMAIL */}
        <input
          type="email"
          name="email"
          placeholder="Correo electrónico"
          value={formik.values.email}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          style={styles.input}
        />
        {formik.touched.email && formik.errors.email && (
          <p style={styles.error}>{formik.errors.email}</p>
        )}

        {/* PASSWORD */}
        <input
          type="password"
          name="password"
          placeholder="Contraseña"
          value={formik.values.password}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          style={styles.input}
        />
        {formik.touched.password && formik.errors.password && (
          <p style={styles.error}>{formik.errors.password}</p>
        )}

        {/* PASSWORD 2 */}
        <input
          type="password"
          name="password2"
          placeholder="Repetir contraseña"
          value={formik.values.password2}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          style={styles.input}
        />
        {formik.touched.password2 && formik.errors.password2 && (
          <p style={styles.error}>{formik.errors.password2}</p>
        )}

        {/* ERROR GLOBAL */}
        {formik.status && <p style={styles.error}>{formik.status}</p>}

        <button
          type="submit"
          style={styles.button}
          disabled={formik.isSubmitting}
        >
          {formik.isSubmitting ? "Registrando..." : "Registrarse"}
        </button>
      </form>

      <p style={styles.text}>
        ¿Ya tienes una cuenta?{" "}
        <span style={styles.link} onClick={() => navigate("/login")}>
          Inicia sesión
        </span>
      </p>
    </div>
  );
};

export default Register;

const styles = {
  container: {
    maxWidth: "400px",
    margin: "50px auto",
    padding: "2rem",
    background: "#1e1e1e",
    borderRadius: "10px",
    color: "#fff",
    textAlign: "center",
  },
  title: {
    marginBottom: "1.5rem",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "1rem",
  },
  input: {
    padding: "10px",
    borderRadius: "5px",
    border: "1px solid #444",
    background: "#2a2a2a",
    color: "#fff",
  },
  button: {
    padding: "10px",
    border: "none",
    borderRadius: "5px",
    background: "var(--allports-700)",
    color: "#fff",
    cursor: "pointer",
  },
  error: {
    color: "#ff5252",
    fontSize: "0.9rem",
  },
  text: {
    marginTop: "1rem",
  },
  link: {
    color: "var(--allports-700)",
    cursor: "pointer",
    textDecoration: "underline",
  },
};

