
import SalidaListPage from "../salida/SalidaListPage";
import SalidaFormPage from "../salida/SalidaFormPage";

const salidaRoutes = [
    {
        path: "/salida",
        element: <SalidaListPage />,
    },
    {
        path: "/salida/:id",
        element: <SalidaFormPage />,
    }
];

export default salidaRoutes
