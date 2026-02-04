import { createContext, useState, useEffect } from "react";
import { login, logout, me, menu as obtenerMenu} from "../api/auth";

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  const [menu, setMenu] = useState([]);

  // --------------------------------------------
  // Inicialización: verificar token (me)
  // --------------------------------------------
  useEffect(() => {
    const inicializarAuth = async () => {
      try {
        const response = await me();
        setUser(response.user);
      } catch (error) {
        // Token inválido / expirado / ausente
        setUser(null);
        console.error("Auth init error:", error);
      } finally {
        if (!user)
          setIsAuthenticated(false)
        else
          setIsAuthenticated(true);
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
  
  // --------------------------------------------
  // Menu
  // --------------------------------------------
  
  useEffect(()=>{
    const getMenu = async()=>{
        try {
          const response = await obtenerMenu();
          setMenu(response);
        }catch(error){
          console.error(error)
          console.log("No se cargó el menu")
        }
    };
    
    getMenu();

  },[])


  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated,
        loading,
        handleLogin,
        handleLogout,
        menu
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
