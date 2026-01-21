import { BrowserRouter, Routes, Route } from "react-router-dom";
import routes from "./runtime/routes";
import Home from "./pages/Home";
import Profile from "./pages/Profile";
import LoginPage from "./pages/LoginPage"
import Register from"./pages/RegisterPage"
import { AuthProvider } from "../src/context/AuthContext";

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<LoginPage />} />
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
