import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

export default function RequireRole({ roles = [], children }) {
  const { user, userRoles = [], loading } = useContext(AuthContext);

  if (loading) return <div>Cargando...</div>;

  if (!user) return <Navigate to="/login" />;

  // Normalizamos a MAYÚSCULAS
  const allowedRoles = roles.map(r => r.toUpperCase());
  const userRolesNormalized = userRoles.map(r => r.toUpperCase());

  // ¿Existe al menos un rol en común?
  const hasPermission = userRolesNormalized.some(role =>
    allowedRoles.includes(role)
  );

  if (!hasPermission) return <h2>No tienes permisos</h2>;

  return children;
}
