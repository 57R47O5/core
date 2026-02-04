import { BrowserRouter, Routes, Route } from "react-router-dom";
import routes from "./runtime/routes";
import Home from "./pages/Home";
import NavBar from "./components/Nav/Nav";
import Profile from "./pages/Profile";
import LoginPage from "./pages/LoginPage"
import Register from"./pages/RegisterPage"
import { AuthProvider } from "../src/context/AuthContext";
import { Sidebar } from "./components/SideBar";

function RutasComunes (){
  
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<Register />} />
    </Routes>    
  )
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <NavBar>
        </NavBar>
        <Sidebar/>
        <RutasComunes/>
        <Routes>
          {routes.map((route, i) => (
            <Route
            key={i}
            path={route.path}
            element={route.element}
            />
          ))}
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
