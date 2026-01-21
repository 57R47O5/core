import React, { useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "@src/pages/LoginPage"
import TurnoCrear from "@src/components/Turnero/TurnoForm";
import TurneroPage from "@src/components/Turnero/TurneroPage";
import TurnoDetalle from "@src/components/Turnero/TurnoDetalle";
import Home from "@src/pages/Home"
import Nav from '@src/components/Nav/Nav';
import { getCookie } from "@src/api/csrf";
import { AuthProvider } from "@src/context/AuthContext";
import UsuarioForm from "@src/components/usuarios/UsuarioForm";
import UsuarioList from "@src/pages/usuarios/UsuarioList";
import PacienteFormPage from "@src/components/pacientes/PacienteFormPage";
import PacientesListPage from "@src/components/pacientes/PacientesListPage";
import RequireRole from "@src/components/RequireRole"


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
          <Route
          path="/usuarios"
          element={
            <RequireRole roles={['MEDICO']}>
              <UsuarioList />
            </RequireRole>
          }
        />
        <Route path="/turnos/nuevo/" element={<TurnoCrear />} />
        <Route path="/turnos/" element={<TurneroPage />} />
        <Route path="/turnos/:id" element={<TurnoDetalle />} />

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
        <Route
          path="/pacientes/nuevo"
          element={
              <PacienteFormPage />
          }
        />
        <Route
          path="/pacientes/:id"
          element={
              <PacienteFormPage />
          }
        />
        <Route
          path="/pacientes/"
          element={
              <PacientesListPage />
          }
        />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
