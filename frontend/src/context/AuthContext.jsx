import { createContext, useState, useEffect } from "react";
import { login, logout, check } from "../api/auth";
import { Alertar, Tipo } from "../utils/alertas";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState();
  const [rol, setRol] = useState(null)
  const [loading, setLoading] = useState(true);

   useEffect(() => {
        const verificarAuth = async () => {
            try {
                const response = await check();
                setIsAuthenticated(response.isAuthenticated);
                setUser(response.user);
                setRol(response.user.rol);
            } catch (error) {
                setIsAuthenticated(false);
                setUser(null);
                setRol(null);
                console.error('Error', error)
                Alertar(error, Tipo.ERROR)
              } finally {
                setLoading(false);
              }
        };

        verificarAuth();
      }, []);
      
      const handleLogin = async (credentials) => {
        try {
          const { user } = await login(credentials);
          setUser(user.username);
          setIsAuthenticated(true)
        }catch(error){
        console.error('Error', error)
        Alertar(error, Tipo.ERROR)
    }

  };
 
  const handleLogout = async () => {
    try {
      await logout();
      setUser(null);
      setIsAuthenticated(false)
      localStorage.removeItem("csrftoken");
    } catch (error) {
      console.error("Error al cerrar sesión:", error);
      Alertar(error, Tipo.ERROR)
    }
  };

  return (
    <AuthContext.Provider value={{ 
      user, setUser, 
      rol, setRol, 
      isAuthenticated, loading, 
      handleLogin, handleLogout  }}>
      {children}
    </AuthContext.Provider>
  );
};
