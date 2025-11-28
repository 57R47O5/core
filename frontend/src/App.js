import React, { useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import Home from "./pages/Home"
import Nav from './components/Nav/Nav';
import { getCookie } from "./api/csrf";
import { AuthProvider } from "./context/AuthContext";
import UsuarioForm from "./components/usuarios/UsuarioForm";
import UsuarioList from "./pages/usuarios/UsuarioList";
import RequireRole from "../src/components/RequireRole"

// import RegisterPage from "./pages/RegisterPage";
// import Profile from "./pages/Profile";
// import CrearCartelPage from "../src/pages/carteles/CrearCartelPage.jsx"

function App() {
  useEffect(() => {
    const fetchToken = async () => {
      const token = getCookie("csrftoken"); 
      if (token) {
        localStorage.setItem("csrftoken", token);
      } else {
        console.warn("No se encontró la cookie csrftoken");
      }
    };
    fetchToken();
  }, []);

  return (
    <AuthProvider>
      <Router>
      <Nav />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<LoginPage />} />
          {/* <Route path="/register" element={<RegisterPage />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/carteles/nuevo" element={<CrearCartelPage />} /> */}
          <Route
          path="/usuarios"
          element={
            <RequireRole roles={['MEDICO']}>
              <UsuarioList />
            </RequireRole>
          }
        />

        <Route
          path="/usuarios/nuevo"
          element={
            <RequireRole roles={['MEDICO']}>
              <UsuarioForm />
            </RequireRole>
          }
        />

        <Route
          path="/usuarios/:id"
          element={
            <RequireRole roles={['MEDICO']}>
              <UsuarioForm />
            </RequireRole>
          }
        />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
