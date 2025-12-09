import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

export default function RequireRole({ roles, children }) {
  const { user, rol, loading } = useContext(AuthContext);

  if (loading) return <div>Cargando...</div>;

  if (!user) return <Navigate to="/login" />;

  if (!roles.includes(rol.toUpperCase())) return <h2>No tienes permisos</h2>;

  return children;
}
