
import MonedaListPage from "../moneda/MonedaListPage";
import MonedaFormPage from "../moneda/MonedaFormPage";

const monedaRoutes = [
    {
        path: "/moneda",
        element: <MonedaListPage />,
    },
    {
        path: "/moneda/:id",
        element: <MonedaFormPage />,
    }
];

export default monedaRoutes
