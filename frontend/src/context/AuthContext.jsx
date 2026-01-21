import { createContext, useState, useEffect } from "react";
import { login, logout, me } from "../api/auth";

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  // --------------------------------------------
  // Inicialización: verificar token (me)
  // --------------------------------------------
  useEffect(() => {
    const inicializarAuth = async () => {
      try {
        const response = await me();
        setUser(response.user);
        setIsAuthenticated(true);
      } catch (error) {
        // Token inválido / expirado / ausente
        setUser(null);
        setIsAuthenticated(false);
        console.error("Auth init error:", error);
      } finally {
        setLoading(false);
      }
    };

    inicializarAuth();
  }, []);

  // --------------------------------------------
  // Login
  // --------------------------------------------
  const handleLogin = async (credentials) => {
    const response = await login(credentials);

    setUser(response.user);
    setIsAuthenticated(true);
  };

  // --------------------------------------------
  // Logout
  // --------------------------------------------
  const handleLogout = async () => {
    await logout();

    setUser(null);
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated,
        loading,
        handleLogin,
        handleLogout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
