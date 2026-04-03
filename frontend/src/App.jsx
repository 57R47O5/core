
import "bootstrap/dist/css/bootstrap.min.css";
import "./styles/app.css"
import { useState, useContext } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import routes from "./runtime/routes";
import Home from "./pages/Home";
import NavBar from "./components/Nav/Nav";
import LoginPage from "./pages/LoginPage"
import Register from"./pages/RegisterPage"
import { AuthContext, AuthProvider } from "../src/context/AuthContext";
import { Sidebar } from "./components/Sidebar";
import AnaliticaDashboardPage from "./apps/elecciones/analitica/AnaliticaDashboardPage";
import { isAuthenticated } from "./api/tokenService";

function RutasComunes (){

  const { isAuthenticated } = useContext(AuthContext);
  
  return (
    <Routes>
      <Route path="/" element={isAuthenticated ? <AnaliticaDashboardPage /> : <Home />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<Register />} />
    </Routes>    
  )
}

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true); 

  return (
    <BrowserRouter>
      <AuthProvider>
        <div className="app-container">
          <NavBar/>

          <div className="app-body">
            <Sidebar 
              isOpen={sidebarOpen} 
              setIsOpen={setSidebarOpen} 
            />

            <main className={`app-main ${sidebarOpen ? "sidebar-open" : ""}`}>
              <RutasComunes/>
              <Routes>
                {routes.map((route, i) => (
                  <Route key={i} path={route.path} element={route.element}/>
                ))}
              </Routes>
            </main>
          </div>

        </div>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
