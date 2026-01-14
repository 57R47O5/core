import Login from "./pages/Login";
import Home from "./pages/Home";

const routes = [
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/",
    element: <Home />,
  },
];

export default routes;
